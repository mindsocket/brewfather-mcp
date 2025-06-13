#!/bin/bash

# Script to analyze ingredient attributes across all debug JSON files
# Usage: ./analyze_ingredient_attributes.sh

OUTPUT_FILE="debug/ingredient_attributes_analysis.txt"
DEBUG_DIR="debug"

echo "Analyzing ingredient attributes from all debug JSON files..." > "$OUTPUT_FILE"
echo "=================================================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Function to analyze a file and extract ingredient attributes
analyze_file() {
    local file="$1"
    local basename=$(basename "$file" .json)
    
    echo "Processing: $file" >&2
    
    # Check what type of file this is and extract ingredient data accordingly
    
    # FERMENTABLES
    if [[ "$basename" == "inventory_fermentables" ]]; then
        echo "=== FERMENTABLES INVENTORY LIST: $basename ===" >> "$OUTPUT_FILE"
        jq -r 'if type == "array" then .[0] | keys | sort | unique | join(", ") else "No fermentables array found" end' "$file" >> "$OUTPUT_FILE"
        
    elif [[ "$basename" =~ ^inventory_fermentables_ ]]; then
        echo "=== FERMENTABLES INVENTORY DETAIL: $basename ===" >> "$OUTPUT_FILE"
        jq -r 'keys | sort | unique | join(", ")' "$file" >> "$OUTPUT_FILE"
    
    # HOPS
    elif [[ "$basename" == "inventory_hops" ]]; then
        echo "=== HOPS INVENTORY LIST: $basename ===" >> "$OUTPUT_FILE"
        jq -r 'if type == "array" then .[0] | keys | sort | unique | join(", ") else "No hops array found" end' "$file" >> "$OUTPUT_FILE"
        
    elif [[ "$basename" =~ ^inventory_hops_ ]]; then
        echo "=== HOPS INVENTORY DETAIL: $basename ===" >> "$OUTPUT_FILE"
        jq -r 'keys | sort | unique | join(", ")' "$file" >> "$OUTPUT_FILE"
        
    # YEASTS
    elif [[ "$basename" == "inventory_yeasts" ]]; then
        echo "=== YEASTS INVENTORY LIST: $basename ===" >> "$OUTPUT_FILE"
        jq -r 'if type == "array" then .[0] | keys | sort | unique | join(", ") else "No yeasts array found" end' "$file" >> "$OUTPUT_FILE"
        
    elif [[ "$basename" =~ ^inventory_yeasts_ ]]; then
        echo "=== YEASTS INVENTORY DETAIL: $basename ===" >> "$OUTPUT_FILE"
        jq -r 'keys | sort | unique | join(", ")' "$file" >> "$OUTPUT_FILE"
        
    # MISCS
    elif [[ "$basename" == "inventory_miscs" ]]; then
        echo "=== MISCS INVENTORY LIST: $basename ===" >> "$OUTPUT_FILE"
        jq -r 'if type == "array" then .[0] | keys | sort | unique | join(", ") else "No miscs array found" end' "$file" >> "$OUTPUT_FILE"
        
    elif [[ "$basename" =~ ^inventory_miscs_ ]]; then
        echo "=== MISCS INVENTORY DETAIL: $basename ===" >> "$OUTPUT_FILE"
        jq -r 'keys | sort | unique | join(", ")' "$file" >> "$OUTPUT_FILE"
        
    # RECIPES
    elif [[ "$basename" =~ ^recipes_ ]]; then
        echo "=== RECIPE CONTEXT: $basename ===" >> "$OUTPUT_FILE"
        
        echo "--- Fermentables:" >> "$OUTPUT_FILE"
        jq -r 'if .fermentables then [.fermentables[] | keys] | add | sort | unique | join(", ") else "No fermentables found" end' "$file" >> "$OUTPUT_FILE"
        
        echo "--- Hops:" >> "$OUTPUT_FILE"
        jq -r 'if .hops then [.hops[] | keys] | add | sort | unique | join(", ") else "No hops found" end' "$file" >> "$OUTPUT_FILE"
        
        echo "--- Yeasts:" >> "$OUTPUT_FILE"
        jq -r 'if .yeasts then [.yeasts[] | keys] | add | sort | unique | join(", ") else "No yeasts found" end' "$file" >> "$OUTPUT_FILE"
        
        echo "--- Miscs:" >> "$OUTPUT_FILE"
        jq -r 'if .miscs then [.miscs[] | keys] | add | sort | unique | join(", ") else "No miscs found" end' "$file" >> "$OUTPUT_FILE"
        
    # BATCHES
    elif [[ "$basename" =~ ^batches_ ]]; then
        echo "=== BATCH CONTEXT: $basename ===" >> "$OUTPUT_FILE"
        
        echo "--- Recipe fermentables:" >> "$OUTPUT_FILE"
        jq -r 'if .recipe.fermentables then [.recipe.fermentables[] | keys] | add | sort | unique | join(", ") else "No recipe.fermentables found" end' "$file" >> "$OUTPUT_FILE"
        
        echo "--- Recipe hops:" >> "$OUTPUT_FILE"
        jq -r 'if .recipe.hops then [.recipe.hops[] | keys] | add | sort | unique | join(", ") else "No recipe.hops found" end' "$file" >> "$OUTPUT_FILE"
        
        echo "--- Recipe yeasts:" >> "$OUTPUT_FILE"
        jq -r 'if .recipe.yeasts then [.recipe.yeasts[] | keys] | add | sort | unique | join(", ") else "No recipe.yeasts found" end' "$file" >> "$OUTPUT_FILE"
        
        echo "--- Recipe miscs:" >> "$OUTPUT_FILE"
        jq -r 'if .recipe.miscs then [.recipe.miscs[] | keys] | add | sort | unique | join(", ") else "No recipe.miscs found" end' "$file" >> "$OUTPUT_FILE"
        
        echo "--- Batch fermentables:" >> "$OUTPUT_FILE"
        jq -r 'if .batchFermentables then [.batchFermentables[] | keys] | add | sort | unique | join(", ") else "No batchFermentables found" end' "$file" >> "$OUTPUT_FILE"
        
        echo "--- Batch hops:" >> "$OUTPUT_FILE"
        jq -r 'if .batchHops then [.batchHops[] | keys] | add | sort | unique | join(", ") else "No batchHops found" end' "$file" >> "$OUTPUT_FILE"
        
        echo "--- Batch yeasts:" >> "$OUTPUT_FILE"
        jq -r 'if .batchYeasts then [.batchYeasts[] | keys] | add | sort | unique | join(", ") else "No batchYeasts found" end' "$file" >> "$OUTPUT_FILE"
        
        echo "--- Batch miscs:" >> "$OUTPUT_FILE"
        jq -r 'if .batchMiscs then [.batchMiscs[] | keys] | add | sort | unique | join(", ") else "No batchMiscs found" end' "$file" >> "$OUTPUT_FILE"
        
    fi
    
    echo "" >> "$OUTPUT_FILE"
}

# Process all JSON files in debug directory
for file in "$DEBUG_DIR"/*.json; do
    if [[ -f "$file" ]]; then
        analyze_file "$file"
    fi
done

echo "Analysis complete. Results saved to: $OUTPUT_FILE"
echo ""
echo "Summary of unique attribute combinations found:"
echo "=============================================="

# Create a summary of unique attribute sets
echo "" >> "$OUTPUT_FILE"
echo "SUMMARY - Unique attribute combinations:" >> "$OUTPUT_FILE"
echo "=======================================" >> "$OUTPUT_FILE"

# Extract just the attribute lines and sort/unique them
grep -E "^[a-zA-Z_].*," "$OUTPUT_FILE" | sort | uniq -c | sort -nr >> "$OUTPUT_FILE"

echo "Full analysis written to: $OUTPUT_FILE"