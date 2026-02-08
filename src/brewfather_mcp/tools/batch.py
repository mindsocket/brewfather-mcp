from datetime import datetime

from brewfather_mcp.api import BrewfatherClient, ListQueryParams
from brewfather_mcp.formatter import format_recipe_details


async def list_batches(client: BrewfatherClient) -> str:
    params = ListQueryParams()
    params.limit = 50
    data = await client.get_batches_list(params)

    formatted_response: list[str] = []
    for item in data.root:
        brew_date_str = (
            datetime.fromtimestamp(item.brew_date / 1000).strftime("%Y-%m-%d %H:%M:%S")
            if item.brew_date
            else "N/A"
        )
        formatted_response.append(
            f"ID: {item.id}\n"
            f"Name: {item.name}\n"
            f"Batch Number: {item.batch_no or 'N/A'}\n"
            f"Status: {item.status or 'N/A'}\n"
            f"Brewer: {item.brewer or 'N/A'}\n"
            f"Brew Date: {brew_date_str}\n"
            f"Recipe Name: {item.recipe_name}\n"
        )
    return "---\n".join(formatted_response) if formatted_response else "No batches found."


async def get_batch_detail(client: BrewfatherClient, batch_id: str) -> str:
    item = await client.get_batch_detail(batch_id)
    brew_date_str = (
        datetime.fromtimestamp(item.brew_date / 1000).strftime("%Y-%m-%d %H:%M:%S")
        if item.brew_date
        else "N/A"
    )
    fermentation_start_str = (
        item.fermentation_start_date.strftime("%Y-%m-%d %H:%M:%S")
        if item.fermentation_start_date
        else "N/A"
    )
    fermentation_end_str = (
        item.fermentation_end_date.strftime("%Y-%m-%d %H:%M:%S")
        if item.fermentation_end_date
        else "N/A"
    )
    bottling_date_str = (
        item.bottling_date.strftime("%Y-%m-%d %H:%M:%S")
        if item.bottling_date
        else "N/A"
    )

    formatted_response = (
        f"Batch Details:\n"
        f"==============\n"
        f"ID: {item.id}\n"
        f"Name: {item.name}\n"
        f"Batch Number: {item.batch_no or 'N/A'}\n"
        f"Status: {item.status or 'N/A'}\n"
        f"Brewer: {item.brewer or 'N/A'}\n"
        f"Brewed: {'Yes' if item.brewed else 'No'}\n"
        f"\nRecipe Information:\n"
        f"------------------\n"
        f"Recipe Name: {getattr(item.recipe, 'name', 'N/A') if item.recipe else 'N/A'}\n"
        f"Recipe ID: {getattr(item.recipe, 'id', getattr(item, 'recipe_id', 'N/A'))}\n"
        f"\nSchedule:\n"
        f"---------\n"
        f"Brew Date: {brew_date_str}\n"
        f"Fermentation Start: {fermentation_start_str}\n"
        f"Fermentation End: {fermentation_end_str}\n"
        f"Bottling Date: {bottling_date_str}\n"
        f"\nGravity & Alcohol:\n"
        f"-----------------\n"
        f"Original Gravity (OG): {item.measured_og or item.og or 'N/A'}\n"
        f"Final Gravity (FG): {item.measured_fg or item.fg or 'N/A'}\n"
        f"ABV: {item.measured_abv or item.abv or 'N/A'}%\n"
        f"\nCarbonation:\n"
        f"-----------\n"
        f"Type: {item.carbonation_type or 'N/A'}\n"
        f"Level: {item.carbonation_level or (item.recipe.carbonation if item.recipe else None) or 'N/A'} volumes\n"
        f"\nTags: {', '.join(item.tags) if item.tags else 'None'}\n"
    )

    brew_measurements = []
    if item.measured_mash_ph:
        target_ph = getattr(item.recipe, 'mash', {}).get('ph') if item.recipe else None
        if target_ph:
            delta = item.measured_mash_ph - target_ph
            brew_measurements.append(f"Mash pH: {item.measured_mash_ph} ({delta:+.2f})")
        else:
            brew_measurements.append(f"Mash pH: {item.measured_mash_ph}")
    if item.measured_first_wort_gravity:
        brew_measurements.append(f"First Wort Gravity: {item.measured_first_wort_gravity}")
    if item.measured_pre_boil_gravity:
        target_pre_boil = getattr(item.recipe, 'pre_boil_gravity', None) if item.recipe else None
        if target_pre_boil:
            delta = item.measured_pre_boil_gravity - target_pre_boil
            brew_measurements.append(f"Pre-Boil Gravity: {item.measured_pre_boil_gravity} ({delta:+.3f})")
        else:
            brew_measurements.append(f"Pre-Boil Gravity: {item.measured_pre_boil_gravity}")
    if item.measured_boil_size:
        target_boil_size = getattr(item.recipe, 'boil_size', None) if item.recipe else None
        if target_boil_size:
            delta = item.measured_boil_size - target_boil_size
            brew_measurements.append(f"Boil Size: {item.measured_boil_size}L ({delta:+.2f}L)")
        else:
            brew_measurements.append(f"Boil Size: {item.measured_boil_size}L")
    if item.measured_post_boil_gravity:
        target_post_boil = getattr(item.recipe, 'post_boil_gravity', None) if item.recipe else None
        if target_post_boil:
            delta = item.measured_post_boil_gravity - target_post_boil
            brew_measurements.append(f"Post-Boil Gravity: {item.measured_post_boil_gravity} ({delta:+.3f})")
        else:
            brew_measurements.append(f"Post-Boil Gravity: {item.measured_post_boil_gravity}")
    if item.measured_kettle_size:
        brew_measurements.append(f"Kettle Size: {item.measured_kettle_size}L")
    if item.measured_og:
        target_og = getattr(item.recipe, 'og', None) if item.recipe else None
        if target_og:
            delta = item.measured_og - target_og
            brew_measurements.append(f"Measured OG: {item.measured_og} ({delta:+.3f})")
        else:
            brew_measurements.append(f"Measured OG: {item.measured_og}")
    if item.measured_batch_size:
        target_batch_size = getattr(item.recipe, 'batch_size', None) if item.recipe else None
        if target_batch_size:
            delta = item.measured_batch_size - target_batch_size
            brew_measurements.append(f"Batch Size: {item.measured_batch_size}L ({delta:+.2f}L)")
        else:
            brew_measurements.append(f"Batch Size: {item.measured_batch_size}L")
    if item.measured_fermenter_top_up:
        brew_measurements.append(f"Fermenter Top-Up: {item.measured_fermenter_top_up}L")

    if brew_measurements:
        formatted_response += "\nBrew Day Measurements:\n---------------------\n"
        for m in brew_measurements:
            formatted_response += f"- {m}\n"

    fermentation_measurements = []
    if item.measured_fg:
        target_fg = getattr(item.recipe, 'fg', None) if item.recipe else None
        if target_fg:
            delta = item.measured_fg - target_fg
            fermentation_measurements.append(f"Measured FG: {item.measured_fg} ({delta:+.3f})")
        else:
            fermentation_measurements.append(f"Measured FG: {item.measured_fg}")
    if item.measured_abv:
        target_abv = getattr(item.recipe, 'abv', None) if item.recipe else None
        if target_abv:
            delta = item.measured_abv - target_abv
            fermentation_measurements.append(f"Measured ABV: {item.measured_abv}% ({delta:+.2f}%)")
        else:
            fermentation_measurements.append(f"Measured ABV: {item.measured_abv}%")
    if item.measured_attenuation:
        target_attenuation = getattr(item.recipe, 'attenuation', None) if item.recipe else None
        if target_attenuation:
            delta = item.measured_attenuation - target_attenuation
            fermentation_measurements.append(f"Measured Attenuation: {item.measured_attenuation}% ({delta:+.2f}%)")
        else:
            fermentation_measurements.append(f"Measured Attenuation: {item.measured_attenuation}%")
    if item.measured_bottling_size:
        fermentation_measurements.append(f"Bottling Size: {item.measured_bottling_size}L")
    if item.measured_efficiency:
        target_efficiency = getattr(item.recipe, 'efficiency', None) if item.recipe else None
        if target_efficiency:
            delta = item.measured_efficiency - target_efficiency
            fermentation_measurements.append(f"Overall Efficiency: {item.measured_efficiency}% ({delta:+.2f}%)")
        else:
            fermentation_measurements.append(f"Overall Efficiency: {item.measured_efficiency}%")
    if item.measured_mash_efficiency:
        target_mash_eff = getattr(item.recipe, 'mash_efficiency', None) if item.recipe else None
        if target_mash_eff:
            delta = item.measured_mash_efficiency - target_mash_eff
            fermentation_measurements.append(f"Mash Efficiency: {item.measured_mash_efficiency}% ({delta:+.2f}%)")
        else:
            fermentation_measurements.append(f"Mash Efficiency: {item.measured_mash_efficiency}%")
    if item.measured_kettle_efficiency:
        fermentation_measurements.append(f"Kettle Efficiency: {item.measured_kettle_efficiency}%")
    if item.measured_conversion_efficiency:
        fermentation_measurements.append(f"Conversion Efficiency: {item.measured_conversion_efficiency}%")

    if fermentation_measurements:
        formatted_response += "\nFermentation Measurements:\n-------------------------\n"
        for m in fermentation_measurements:
            formatted_response += f"- {m}\n"

    if item.notes:
        formatted_response += "\nNotes:\n"
        for note in item.notes:
            note_time = datetime.fromtimestamp(note.timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")
            formatted_response += f"- [{note.type}] {note.note} ({note_time})\n"

    if item.measurements:
        formatted_response += "\nMeasurements:\n-------------\n"
        for measurement in item.measurements:
            meas_time = measurement.time.strftime("%Y-%m-%d %H:%M:%S") if hasattr(measurement, 'time') and measurement.time else "N/A"
            comment = f" ({measurement.comment})" if hasattr(measurement, 'comment') and measurement.comment else ""
            formatted_response += f"- {measurement.type}: {measurement.value} {measurement.unit} [{meas_time}]{comment}\n"

    if item.measurement_devices:
        formatted_response += "\nMeasurement Devices:\n------------------\n"
        for device in item.measurement_devices:
            device_name = device.get('name', 'Unknown Device')
            device_type = device.get('type', 'N/A')
            formatted_response += f"- {device_name} ({device_type})\n"

    if item.recipe:
        formatted_response += "\n\n" + "=" * 50 + "\n"
        formatted_response += "RECIPE DETAILS\n"
        formatted_response += "=" * 50 + "\n\n"
        formatted_response += format_recipe_details(item.recipe)

    formatted_response += "\n\nBatch Metadata:\n--------------\n"
    formatted_response += f"Batch ID: {item.id}\n"

    return formatted_response


async def update_batch(client: BrewfatherClient, batch_id: str, update_data: dict) -> str:
    if not update_data:
        return "No update parameters provided."
    await client.update_batch_detail(batch_id, update_data)
    return f"Batch {batch_id} updated successfully."


async def get_batch_brewtracker(client: BrewfatherClient, batch_id: str) -> str:
    tracker = await client.get_batch_brewtracker(batch_id)

    if not tracker.name or not tracker.stages:
        return f"No brewtracker data available for batch {batch_id}. This batch may not have brewing process tracking enabled."

    formatted_response = (
        f"BREWING PROCESS TRACKER: {tracker.name}\n"
        f"{'=' * 60}\n\n"
        f"Status: {'ACTIVE' if tracker.active else 'INACTIVE'} | Stage {tracker.stage + 1} of {len(tracker.stages)}\n"
        f"Completed: {'Yes' if tracker.completed else 'No'} | Notifications: {'On' if tracker.notify else 'Off'}\n\n"
    )

    for i, stage in enumerate(tracker.stages):
        status_icon = "🔄" if i == tracker.stage and tracker.active else "✅" if i < tracker.stage else "⏳"
        formatted_response += f"{status_icon} STAGE {i + 1}: {stage.name.upper()}\n"
        formatted_response += f"Duration: {stage.duration // 60} min | Current Step: {stage.step + 1}/{len(stage.steps)}\n"
        formatted_response += f"Position: {stage.position // 60} min {'(PAUSED)' if stage.paused else ''}\n\n"

        for j, step in enumerate(stage.steps):
            step_icon = "▶️" if i == tracker.stage and j == stage.step and tracker.active else "✅" if j < stage.step or i < tracker.stage else "⏸️"
            step_name = step.name if step.name else f"{step.type.title()} Step"
            formatted_response += f"  {step_icon} {step_name}"

            if step.time > 0:
                formatted_response += f" @ {step.time // 60} min"
            if step.value:
                formatted_response += f" ({step.value}°C)"
            formatted_response += "\n"

            if step.description:
                formatted_response += f"     📝 {step.description}\n"

            if step.tooltip and step.tooltip != step.description:
                formatted_response += f"     💡 {step.tooltip}\n"

            if i == tracker.stage and j == stage.step and tracker.active and step.start_time and step.duration:
                try:
                    current_time = int(datetime.now().timestamp() * 1000)
                    elapsed_ms = current_time - step.start_time
                    elapsed_seconds = elapsed_ms / 1000
                    remaining_seconds = step.duration - elapsed_seconds

                    if remaining_seconds > 0:
                        remaining_minutes = int(remaining_seconds // 60)
                        remaining_secs = int(remaining_seconds % 60)
                        elapsed_minutes = int(elapsed_seconds // 60)
                        elapsed_secs = int(elapsed_seconds % 60)
                        formatted_response += f"     ⏱️  Elapsed: {elapsed_minutes}:{elapsed_secs:02d} | Remaining: {remaining_minutes}:{remaining_secs:02d}\n"
                    else:
                        formatted_response += f"     ⏰  Step should have completed! ({int(elapsed_seconds // 60)} min elapsed)\n"
                except Exception:
                    pass

            formatted_response += "\n"

        formatted_response += "\n"

    return formatted_response


async def get_batch_last_reading(client: BrewfatherClient, batch_id: str) -> str:
    reading = await client.get_batch_last_reading(batch_id)

    reading_time = datetime.fromtimestamp(reading.time / 1000).strftime("%Y-%m-%d %H:%M:%S")

    formatted_response = (
        f"LATEST SENSOR READING\n"
        f"{'=' * 40}\n\n"
        f"Device: {reading.name} ({reading.device_type})\n"
        f"Reading Time: {reading_time}\n"
        f"Device ID: {reading.id}\n\n"
        f"MEASUREMENTS:\n"
        f"-------------"
    )

    if reading.temp is not None:
        formatted_response += f"\n🌡️  Temperature: {reading.temp}°C"
    if reading.sg is not None:
        formatted_response += f"\n🍺  Specific Gravity: {reading.sg:.4f}"
    if reading.battery is not None:
        battery_icon = "🔋" if reading.battery > 50 else "🪫" if reading.battery > 20 else "🚨"
        formatted_response += f"\n{battery_icon}  Battery: {reading.battery:.1f}%"
    if reading.rssi is not None:
        signal_icon = "📶" if reading.rssi > -50 else "📊" if reading.rssi > -70 else "📱"
        formatted_response += f"\n{signal_icon}  Signal: {reading.rssi:.1f} dBm"
    if reading.target_temp is not None:
        formatted_response += f"\n🎯  Target Temp: {reading.target_temp}°C"
    if reading.ph is not None:
        formatted_response += f"\n🧪  pH: {reading.ph}"
    if reading.pressure is not None:
        formatted_response += f"\n⚡  Pressure: {reading.pressure}"

    return formatted_response


async def get_batch_readings_summary(client: BrewfatherClient, batch_id: str, limit: int = 10) -> str:
    readings = await client.get_batch_readings(batch_id)

    if not readings.root:
        return "No sensor readings found for this batch."

    recent_readings = readings.root[-limit:] if len(readings.root) > limit else readings.root

    formatted_response = (
        f"RECENT SENSOR READINGS SUMMARY\n"
        f"{'=' * 50}\n\n"
        f"Total readings available: {len(readings.root)}\n"
        f"Showing latest {len(recent_readings)} readings:\n\n"
    )

    for reading in recent_readings:
        reading_time = datetime.fromtimestamp(reading.time / 1000).strftime("%m-%d %H:%M")
        device_name = reading.name or reading.id or reading.type or "Unknown Device"
        line = f"{reading_time} | {device_name}"

        if reading.temp is not None:
            line += f" | {reading.temp:.1f}°C"
        if reading.sg is not None:
            line += f" | SG {reading.sg:.4f}"
        if reading.battery is not None:
            line += f" | {reading.battery:.0f}%"

        formatted_response += line + "\n"

    if len(recent_readings) >= 3:
        formatted_response += "\nTREND ANALYSIS:\n"
        first = recent_readings[0]
        last = recent_readings[-1]

        if first.temp is not None and last.temp is not None:
            temp_change = last.temp - first.temp
            temp_trend = "↗️ Rising" if temp_change > 0.5 else "↘️ Falling" if temp_change < -0.5 else "➡️ Stable"
            formatted_response += f"Temperature: {temp_trend} ({temp_change:+.1f}°C)\n"

        if first.sg is not None and last.sg is not None:
            sg_change = last.sg - first.sg
            sg_trend = "↗️ Rising" if sg_change > 0.002 else "↘️ Falling" if sg_change < -0.002 else "➡️ Stable"
            formatted_response += f"Specific Gravity: {sg_trend} ({sg_change:+.4f})\n"

    return formatted_response
