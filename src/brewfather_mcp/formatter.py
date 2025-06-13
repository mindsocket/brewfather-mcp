"""Shared recipe formatting utilities."""

from brewfather_mcp.types import RecipeDetail

def format_recipe_details(recipe: RecipeDetail, section_title: str = "RECIPE DETAILS") -> str:
    """Format recipe details into a comprehensive string representation.
    
    Args:
        recipe: The RecipeDetail object to format
        section_title: Optional title for the section (used in batch output)
    
    Returns:
        Formatted string with complete recipe information
    """
    # Basic recipe info
    created_date = recipe.created.to_datetime().strftime("%Y-%m-%d %H:%M:%S") if recipe.created else "N/A"
    last_modified = recipe.timestamp.to_datetime().strftime("%Y-%m-%d %H:%M:%S") if recipe.timestamp else "N/A"
    
    formatted_response = f"""Recipe: {recipe.name}
Author: {recipe.author or 'N/A'}
Type: {recipe.type or 'N/A'}
Created: {created_date}
Last Modified: {last_modified}
Public: {recipe.public if recipe.public is not None else 'N/A'}
Tags: {', '.join(recipe.tags) if recipe.tags else 'None'}

Style Information:
-----------------
Name: {recipe.style.name if recipe.style else 'N/A'}
Category: {getattr(recipe.style, 'category', 'N/A')}
Type: {getattr(recipe.style, 'type', 'N/A')}
Style Guide: {getattr(recipe.style, 'style_guide', 'N/A')}
Conformity: {'Yes' if recipe.style_conformity else 'No'}

Specifications:
--------------
Batch Size: {recipe.batch_size}L
Boil Size: {recipe.boil_size}L
Boil Time: {recipe.boil_time} minutes
Brewhouse Efficiency: {recipe.efficiency}%
Mash Efficiency: {recipe.mash_efficiency}%
Original Gravity: {recipe.og} ({recipe.og_plato or 'N/A'}°P)
Final Gravity: {recipe.fg}
IBU: {recipe.ibu} (Formula: {recipe.ibu_formula})
Color: {recipe.color} SRM
ABV: {recipe.abv}%
Attenuation: {recipe.attenuation}%
BU:GU Ratio: {recipe.bu_gu_ratio}
Carbonation: {recipe.carbonation or 'N/A'} volumes
Pre-Boil Gravity: {recipe.pre_boil_gravity or 'N/A'}
Post-Boil Gravity: {recipe.post_boil_gravity}

Process Details:
---------------
FG Formula: {getattr(recipe, 'fg_formula', 'N/A')}
Carbonation Type: {getattr(recipe, 'carbonation_type', 'N/A')}
Primary Temp: {getattr(recipe, 'primary_temp', 'N/A')}°C
First Wort Gravity: {getattr(recipe, 'first_wort_gravity', 'N/A')}
Diastatic Power: {getattr(recipe, 'diasmatic_power', 'N/A')}
Hopstand Temp: {getattr(recipe, 'avg_weighted_hopstand_temp', 'N/A')}°C
Dry Hop Rate: {getattr(recipe, 'sum_dry_hop_per_liter', 'N/A')}g/L

Ingredient Totals:
-----------------
Total Fermentables: {recipe.fermentables_total_amount}kg
Total Hops: {recipe.hops_total_amount}g

Equipment Profile:
----------------
Name: {recipe.equipment.name if recipe.equipment else 'N/A'}

Fermentables:
------------
"""
    for ferm in recipe.fermentables:
        formatted_response += f"{ferm.name}: {ferm.amount}kg ({ferm.percentage}%) - {ferm.type}\n"

    formatted_response += "\nHops Schedule:\n-------------\n"
    for hop in recipe.hops:
        formatted_response += f"{hop.name}: {hop.amount}g ({hop.alpha}% AA) - {hop.use} for {hop.time} min @ {hop.temp or 100}°C\n"

    formatted_response += "\nYeast:\n------\n"
    for yeast in recipe.yeasts:
        formatted_response += f"{yeast.name} ({yeast.laboratory}) - {yeast.amount} {yeast.unit or 'pkg'}\n"
        formatted_response += f"Form: {yeast.form}, Attenuation: {yeast.attenuation}%\n"

    if recipe.miscs:
        formatted_response += "\nMiscellaneous:\n-------------\n"
        for misc in recipe.miscs:
            formatted_response += f"{misc.name}: {misc.amount} {misc.unit or 'g'} - {misc.use}"
            if misc.time is not None:
                formatted_response += f" @ {misc.time} {'days' if misc.time_is_days else 'min'}"
            formatted_response += "\n"

    # Add boil steps if available
    if hasattr(recipe, 'boil_steps') and recipe.boil_steps:
        formatted_response += "\nBoil Schedule:\n-------------\n"
        for step in recipe.boil_steps:
            formatted_response += f"@ {step.time} min: {step.name}\n"
    
    # Add mash profile if available
    if recipe.mash:
        formatted_response += "\nMash Profile:\n------------\n"
        if hasattr(recipe.mash, 'steps'):
            # It's a MashSchedule object
            formatted_response += f"Name: {recipe.mash.name}\n"
            for i, step in enumerate(recipe.mash.steps, 1):
                formatted_response += f"Step {i}: {step.type} - {step.step_temp}°C for {step.step_time} min"
                if step.ramp_time:
                    formatted_response += f" (ramp: {step.ramp_time} min)"
                formatted_response += "\n"
        elif isinstance(recipe.mash, dict) and 'steps' in recipe.mash:
            # It's a dict (backward compatibility)
            for i, step in enumerate(recipe.mash['steps'], 1):
                temp = step.get('stepTemp', 'N/A')
                time = step.get('stepTime', 'N/A')
                step_type = step.get('type', 'Infusion')
                formatted_response += f"Step {i}: {step_type} - {temp}°C for {time} min\n"
    
    if recipe.water:
        formatted_response += "\nWater Profile:\n-------------\n"
        formatted_response += f"Source Water: {recipe.water.source.name}\n"
        formatted_response += f"Mash pH: {recipe.water.mash_ph}\n"
        if recipe.water.acid_ph_adjustment:
            formatted_response += f"Acid pH Adjustment: {recipe.water.acid_ph_adjustment}\n"
        
        formatted_response += "\nSource Profile (mg/L):\n"
        sp = recipe.water.source
        formatted_response += f"Ca: {sp.calcium} Mg: {sp.magnesium} Na: {sp.sodium} "
        formatted_response += f"Cl: {sp.chloride} SO4: {sp.sulfate} HCO3: {sp.bicarbonate}\n"
        
        formatted_response += "\nTarget Profile (mg/L):\n"
        wp = recipe.water.total
        formatted_response += f"Ca: {wp.calcium} Mg: {wp.magnesium} Na: {wp.sodium} "
        formatted_response += f"Cl: {wp.chloride} SO4: {wp.sulfate} HCO3: {wp.bicarbonate}\n"
        
        # Add water adjustments
        ma = recipe.water.mash_adjustments
        if any([ma.calcium_chloride, ma.calcium_sulfate, ma.magnesium_sulfate, ma.sodium_chloride, ma.sodium_bicarbonate]):
            formatted_response += "\nMash Adjustments (g):\n"
            if ma.calcium_chloride: formatted_response += f"CaCl2: {ma.calcium_chloride}g\n"
            if ma.calcium_sulfate: formatted_response += f"CaSO4: {ma.calcium_sulfate}g\n"
            if ma.magnesium_sulfate: formatted_response += f"MgSO4: {ma.magnesium_sulfate}g\n"
            if ma.sodium_chloride: formatted_response += f"NaCl: {ma.sodium_chloride}g\n"
            if ma.sodium_bicarbonate: formatted_response += f"NaHCO3: {ma.sodium_bicarbonate}g\n"

    if recipe.fermentation:
        formatted_response += "\nFermentation Schedule:\n--------------------\n"
        formatted_response += f"Profile: {recipe.fermentation.name}\n"
        for i, step in enumerate(recipe.fermentation.steps, 1):
            formatted_response += f"Step {i}: {step.type} - {step.step_temp}°C for {step.step_time} days"
            if hasattr(step, 'actual_time') and step.actual_time:
                from datetime import datetime
                actual_date = datetime.fromtimestamp(step.actual_time / 1000).strftime('%Y-%m-%d')
                formatted_response += f" (started: {actual_date})"
            formatted_response += "\n"

    if recipe.notes:
        formatted_response += f"\nNotes:\n------\n{recipe.notes}\n"
        
    # Add efficiency calculations if available
    if hasattr(recipe, 'rb_ratio') and recipe.rb_ratio:
        formatted_response += f"\nAdvanced Calculations:\n---------------------\n"
        formatted_response += f"RB Ratio: {recipe.rb_ratio}\n"
        if hasattr(recipe, 'total_gravity'):
            formatted_response += f"Total Gravity: {recipe.total_gravity}\n"
        if hasattr(recipe, 'extra_gravity'):
            formatted_response += f"Extra Gravity: {recipe.extra_gravity}\n"
    
    # Add version and metadata
    formatted_response += f"\nMetadata:\n---------\n"
    formatted_response += f"Recipe ID: {recipe.id}\n"
    formatted_response += f"Version: {recipe.version}\n"
    formatted_response += f"Revision: {recipe.rev}\n"
    if hasattr(recipe, 'search_tags') and recipe.search_tags:
        formatted_response += f"Search Tags: {', '.join(recipe.search_tags)}\n"
    
    return formatted_response