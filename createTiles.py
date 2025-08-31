import os
import math
import json
from PIL import Image,ImageColor

def generate_osm_tiles_from_json(json_file_path, zoom, tile_size, output_dir):
    """
    Generates OpenStreetMap-like tiles with colored circles by reading data
    from a JSON file.
    """
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        print(f"Error: The file '{json_file_path}' does not exist.")
        return

    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading JSON from file '{json_file_path}': {e}")
        return

    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        print("Error: JSON data must be a list of objects.")
        return

    os.makedirs(output_dir, exist_ok=True)

    def lat_to_mercator(lat):
        """Converts latitude to Mercator projection coordinate."""
        # Clamp latitude to avoid math domain errors near the poles
        # The valid range for Mercator projection is approx. -85.05 to +85.05 degrees
        max_lat = 85.05112878
        lat = max(-max_lat, min(lat, max_lat))
        return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

    def deg_to_tile(lat, lon, zoom):
        """Converts WGS84 degrees to a tile and pixel coordinate."""
        n = 2 ** zoom
        
        # Calculate x tile and pixel
        x_tile_float = n * ((lon + 180) / 360)
        x_tile = math.floor(x_tile_float)
        x_pixel = int((x_tile_float - x_tile) * tile_size)

        # Calculate y tile and pixel
        y_tile_float = n * (1 - lat_to_mercator(lat) / math.pi) / 2
        y_tile = math.floor(y_tile_float)
        y_pixel = int((y_tile_float - y_tile) * tile_size)
        
        return x_tile, y_tile, x_pixel, y_pixel

    multiplication_factor = 0.0001757812499931788
    tile_data = {}

    for item in data:
        try:
            raw_lat = item['y']
            raw_lon = item['x']
            color = item['color']
            
            lat = raw_lat * multiplication_factor
            lon = raw_lon * multiplication_factor
        except KeyError as e:
            print(f"Warning: Skipping item due to missing key: {e}")
            continue

        # We will now handle the potential error at the deg_to_tile call.
        try:
            x_tile, y_tile, x_pixel, y_pixel = deg_to_tile(lat, lon, zoom)
        except ValueError:
            print(f"Warning: Skipping point ({raw_lat}, {raw_lon}) with multiplied coordinates ({lat}, {lon}) due to out-of-bounds latitude for Mercator projection.")
            continue
        
        if (x_tile, y_tile) not in tile_data:
            tile_data[(x_tile, y_tile)] = []
        tile_data[(x_tile, y_tile)].append({'x': x_pixel, 'y': y_pixel, 'color': color})

    # Generate the images for each tile
    for (x, y), points in tile_data.items():
        img = Image.new('RGB', (tile_size, tile_size), 'white')
        
        for point in points:
            r = 10  # Radius of the circle
            x_pos = point['x']
            y_pos = point['y']
            
            for i in range(x_pos - r, x_pos + r + 1):
                for j in range(y_pos - r, y_pos + r + 1):
                    if (i - x_pos)**2 + (j - y_pos)**2 <= r**2:
                        if 0 <= i < tile_size and 0 <= j < tile_size:
                            if point['color'] == 'None':
                                img.putpixel((i, j), (0, 0, 0))
                                continue
                            try:
                                img.putpixel((i, j), ImageColor.getrgb(point['color']))
                            except ValueError:
                                print(f"Warning: Invalid color name/hex '{point['color']}'. Using black.")
                                img.putpixel((i, j), (0, 0, 0))

        tile_dir = os.path.join(output_dir, str(zoom), str(x))
        os.makedirs(tile_dir, exist_ok=True)
        
        filename = os.path.join(tile_dir, f"{y}.png")
        img.save(filename)
        print(f"Generated tile: {filename}")

# --- Example Usage ---

if __name__ == "__main__":
    json_data_file = "wplace.json"
    json_data_file = "ScrapeWPLACE\output.json"
    zoom_level = 15
    tile_size_pixels = 256
    output_directory = "data"


    generate_osm_tiles_from_json(json_data_file, zoom_level, tile_size_pixels, output_directory)
    print("\nTile generation complete.")
    print(f"Check the '{output_directory}' directory to see the generated tiles.")
    print("The files are organized in the format: <output_dir>/<zoom>/<x>/<y>.png")
