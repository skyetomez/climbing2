import pandas as pd
import overpy
import argparse


def get_climbing_centers(name: str) -> None:
    api = overpy.Overpass()
    query = f"""
    [out:json];
    area["name:en"="{name}"];
    node["leisure"="sports_centre"]["sport"="climbing"](area);
    out center;
    """

    try:
        result = api.query(query)
        print(result)
        print(result.nodes)
    except overpy.exception.OverpassBadRequest as e:
        print(f"OverpassBadRequest: {e}")

    locations = []

    for node in result.nodes:
        location = {
            'name': node.tags.get('name'),
            'lat': node.lat,
            'lon': node.lon,
            'type': 'node'
        }
        locations.append(location)

    climbing_locations_df = pd.DataFrame(
        locations,
        columns=['name', 'lat', 'lon', 'type']
    )

    climbing_locations_df.to_csv(
        f'{name.lower()}_climbing_locations.csv', index=False)


def get_coordinates(fname: str) -> dict:
    df = pd.read_csv(fname)

    coordinates = dict()

    for _, row in df.iterrows():

        lat, long = row['lat'], row['lon']
        name = row["name"]
        coordinates[(lat, long)] = name

    return coordinates


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get climbing centers')
    parser.add_argument('name', type=str, help='Country or city eg. Spain')
    args = parser.parse_args()
    get_climbing_centers(args.name)
