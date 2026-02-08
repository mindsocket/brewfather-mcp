---
name: brewfather-cli
description: Manage Brewfather homebrewing data — inventory, batches, recipes. Use when working on beer making.
allowed-tools: Bash(brewfather-cli:*)
---

Use `brewfather-cli` to interact with Brewfather brewing data. List and detail commands support `--help` and `--json` for raw API output.

## Authentication

```bash
brewfather-cli auth configure       # Interactive setup (prompts for credentials)
brewfather-cli auth status          # Validate connection
```

Credentials: env vars `BREWFATHER_API_USER_ID` / `BREWFATHER_API_KEY`, or `~/.config/brewfather-cli/auth.json`.

## Inventory

```bash
brewfather-cli inventory summary                        # All inventory overview
brewfather-cli inventory fermentable list               # Fermentables in stock
brewfather-cli inventory fermentable detail <id>        # Fermentable details
brewfather-cli inventory fermentable update <id> <kg>   # Set amount (kg)
brewfather-cli inventory hop list                       # Hops in stock
brewfather-cli inventory hop detail <id>                # Hop details
brewfather-cli inventory hop update <id> <grams>        # Set amount (g)
brewfather-cli inventory yeast list                     # Yeasts in stock
brewfather-cli inventory yeast detail <id>              # Yeast details
brewfather-cli inventory yeast update <id> <packets>    # Set amount (packets)
brewfather-cli inventory misc list                      # Misc items in stock
brewfather-cli inventory misc detail <id>               # Misc item details
brewfather-cli inventory misc update <id> <units>       # Set amount (units)
```

## Batches

```bash
brewfather-cli batch list                               # All batches
brewfather-cli batch detail <id>                        # Batch details + recipe
brewfather-cli batch update <id> --status Fermenting    # Update status
brewfather-cli batch update <id> --measured-og 1.052    # Update measurements
brewfather-cli batch brewtracker <id>                   # Brewing process tracker for use on brew day
brewfather-cli batch last-reading <id>                  # Latest sensor reading for use during fermentation
brewfather-cli batch readings <id> [--limit N]          # Recent sensor readings
```

## Recipes

```bash
brewfather-cli recipe list          # All recipes
brewfather-cli recipe detail <id>   # Full recipe details
brewfather-cli recipe enums         # Valid enum values for recipe creation
```
