from models.storage.layers.trusted import Trusted
from rapidfuzz import process, fuzz
import pandas as pd
import numpy as np


class MVCVehicles(Trusted):
    def _get_trusted_table_name(self) -> str:
        return "mvc_vehicles"

    def _list_tables(self) -> list[str]:
        return list(
            filter(
                lambda x: "motorvehiclecollisionsvehicles" in x,
                self.formatted_db_connector.get_tables(),
            )
        )

    def _clean_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop_duplicates("collision_id")
        return df.reset_index()

    def _correct_misspellings(self, df: pd.DataFrame) -> pd.DataFrame:
        vehicle_type_choices = [
            "2-Door Sedan",
            "3-Door Vehicle",
            "4-Door Sedan",
            "All-Terrain Vehicle",
            "Ambulance",
            "Armored Truck",
            "Backhoe Loader",
            "Beverage Truck",
            "Bike",
            "Bicycle",
            "Bobcat",
            "Boom Lift",
            "Box Truck",
            "Bulldozer",
            "Bus",
            "Camper Van",
            "Car Carrier",
            "Cargo Van",
            "Carriage",
            "Cement Mixer",
            "Cherry Picker",
            "City Vehicle",
            "Concrete Mixer",
            "Construction Vehicle",
            "Convertible",
            "Courier Van",
            "Crane",
            "Delivery Truck",
            "Dirt Bike",
            "Dump Truck",
            "Electric Bike (E-Bike)",
            "Electric Scooter (E-Scooter)",
            "Excavator",
            "Fire Engine",
            "Fire Truck",
            "Flatbed Truck",
            "Forklift",
            "Garbage Truck",
            "Golf Cart",
            "Government Vehicle",
            "Grain Truck",
            "Hearse",
            "Horse Carriage",
            "Ice Cream Truck",
            "Jet Ski",
            "Ladder Truck",
            "Lawn Mower",
            "Lift Boom",
            "Limousine",
            "Livestock Rack",
            "Mail Truck",
            "Minibike",
            "Minivan",
            "Moped",
            "Motor Home",
            "Motor Scooter",
            "Motorcycle",
            "Omnibus",
            "Open Body Truck",
            "Other",
            "Passenger Vehicle",
            "Pedicab",
            "Pickup Truck",
            "Police Vehicle",
            "Postal Vehicle",
            "Power Shovel",
            "Refrigerated Van",
            "Road Sweeper",
            "Scooter",
            "Sedan",
            "Semi-Trailer",
            "Skateboard",
            "Skid Steer Loader",
            "Snow Plow",
            "Special Purpose Vehicle",
            "Sport Utility Vehicle (SUV)",
            "Stake Truck",
            "Station Wagon",
            "Street Sweeper",
            "Suburban",
            "Sweeper Truck",
            "Tank Truck",
            "Taxi",
            "Tow Truck",
            "Tractor",
            "Tractor Trailer",
            "Trailer",
            "Trash Truck",
            "Truck",
            "Utility Vehicle",
            "Van",
            "Wheelchair",
            "Work Van",
            "Unknown Vehicle",
        ]
        vehicle_make_choices = [
            "Alfa Romeo",
            "Ankai",
            "Apollo",
            "Autocar",
            "Big Dog",
            "Blue Bird",
            "Bobcat",
            "Bombardier",
            "Can-Am",
            "Caterpillar",
            "Chevrolet",
            "Chrysler",
            "Club Car",
            "Collins Bus",
            "Crane Carrier",
            "Dodge",
            "E-One",
            "Ferrara",
            "Ford",
            "Freightliner",
            "Genuine Scooters",
            "Gillig",
            "Great Dane",
            "Grumman",
            "Harley-Davidson",
            "Hino",
            "Honda",
            "Hyundai",
            "IC Bus",
            "International",
            "Isuzu",
            "JLG",
            "John Deere",
            "Kenworth",
            "KME",
            "Kubota",
            "Kymco",
            "Liebherr",
            "Mack",
            "Manitou",
            "Mercedes-Benz",
            "MCI",
            "Mini",
            "Mitsubishi",
            "Navistar International",
            "New Flyer",
            "Nissan",
            "Nova Bus",
            "Orion",
            "Oshkosh",
            "Peterbilt",
            "Pierce",
            "Polaris",
            "Prevost",
            "RAM",
            "Rosenbauer",
            "Seagrave",
            "Setra",
            "Sterling",
            "Thomas Built Buses",
            "Toyota",
            "Triumph",
            "U-Haul",
            "Utility Trailer Manufacturing Company",
            "Van Hool",
            "Vauxhall",
            "Volvo",
            "Western Star",
            "Workhorse",
            "Yamaha",
            "Alexander Dennis",
            "Case",
            "Cushman",
            "E-Z-GO",
            "Genie",
            "Grove",
            "Hyster",
            "JCB",
            "Komatsu",
            "Manac",
            "Terex",
            "Piaggio",
            "Bajaj",
            "Daewoo",
            "Fiat",
            "Suzuki",
            "Kawasaki",
            "Victory",
            "MV Agusta",
            "Benelli",
            "Aprilia",
            "SYM",
            "Mahindra",
            "Foton",
            "Hyosung",
            "GMC",
            "Scania",
            "Renault",
            "Iveco",
            "DAF",
            "Dennis",
            "Tesla",
            "Lucid",
            "Rivian",
            "BYD",
            "Proterra",
            "Marcopolo",
            "Neoplan",
            "Optare",
            "Solaris",
            "Temsa",
            "Yutong",
            "Zhongtong",
            "King Long",
            "Ashok Leyland",
            "Tata",
            "Mazda",
            "Subaru",
            "Jeep",
            "Land Rover",
            "Jaguar",
            "Cadillac",
            "Buick",
            "Lincoln",
            "Chery",
            "Geely",
            "Haval",
            "Saab",
            "Skoda",
            "Seat",
            "Ducati",
            "Husqvarna",
            "Bimota",
            "Gas Gas",
            "Royal Enfield",
            "Zero Motorcycles",
            "Energica",
            "Niu",
            "Segway",
            "Ninebot",
            "Bird",
            "Lime",
            "Boosted",
            "Gotrax",
            "Emove",
            "Kaabo",
            "Dualtron",
            "Varla",
            "Nanrobot",
            "Xiaomi",
            "Inokim",
            "Glion",
            "Razor",
            "E-Twow",
            "Swagtron",
            "Mercane",
            "SoFlow",
            "Unagi",
            "EV Rider",
            "Hover-1",
            "Qiewa",
            "Kugoo",
            "Vsett",
            "Surron",
            "Super73",
            "Rad Power Bikes",
            "VanMoof",
            "Juiced Bikes",
            "Aventon",
            "Lectric",
            "Cowboy",
            "Brompton",
            "Gazelle",
            "Yuba",
            "Tern",
            "Blix",
            "Pedego",
            "Ancheer",
            "Flyer",
            "Electric Bike Company",
            "Addmotor",
            "Haibike",
            "Frey",
            "Riese & Müller",
            "Bianchi",
            "Specialized",
            "Giant",
            "Trek",
            "Cannondale",
            "Santa Cruz",
            "Scott",
            "Orbea",
            "KTM",
            "Canyon",
            "Merida",
            "Cube",
            "Ghost",
            "Polygon",
        ]

        vehicle_type_choices_clean = [v.lower() for v in vehicle_type_choices]
        vehicle_make_choices_clean = [v.lower() for v in vehicle_make_choices]

        df["vehicle_type_clean"] = (
            df["vehicle_type"].astype(str).str.lower().str.strip()
        )
        df["vehicle_make_clean"] = (
            df["vehicle_make"].astype(str).str.lower().str.strip()
        )

        def get_best_match(series, choices_clean, scorer=fuzz.WRatio, score_cutoff=80):
            matches = process.cdist(
                series.tolist(), choices_clean, scorer=scorer, score_cutoff=score_cutoff
            )
            best_matches = []
            for i, match_list in enumerate(matches):
                if len(match_list):
                    best_match = np.argmax(match_list)
                    original_choice = choices_clean[best_match]
                    best_matches.append(original_choice)
                else:
                    best_matches.append("Unknown Vehicle")
            return best_matches

        df["vehicle_type"] = get_best_match(
            df["vehicle_type_clean"], vehicle_type_choices_clean
        )
        df["vehicle_make"] = get_best_match(
            df["vehicle_make_clean"], vehicle_make_choices_clean
        )

        df = df.drop(columns=["vehicle_type_clean", "vehicle_make_clean"])
        return df

    def _format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        def transform_vehicle_damage_to_onehot(df: pd.DataFrame) -> pd.DataFrame:
            df["vehicle_damage_combined"] = df[
                [
                    "vehicle_damage",
                    "vehicle_damage_1",
                    "vehicle_damage_2",
                    "vehicle_damage_3",
                ]
            ].apply(lambda row: row.dropna().tolist(), axis=1)
            df = df.drop(
                [
                    "vehicle_damage",
                    "vehicle_damage_1",
                    "vehicle_damage_2",
                    "vehicle_damage_3",
                ],
                axis=1,
            )
            df = pd.concat(
                [
                    df,
                    pd.get_dummies(df["vehicle_damage_combined"].explode())
                    .groupby(level=0)
                    .sum(),
                ],
                axis=1,
            )
            return df.drop("vehicle_damage_combined", axis=1)

        def transform_datetime_to_utc(df: pd.DataFrame) -> pd.DataFrame:
            df["crash_datetime"] = pd.to_datetime(
                df["crash_date"] + " " + df["crash_time"]
            )
            return df.drop(["crash_date", "crash_time"], axis=1)

        df = transform_vehicle_damage_to_onehot(df)
        df = self._transform_column_names_to_snake_case(df)
        df = transform_datetime_to_utc(df)
        return df

    def _drop_insignificant_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(
            [
                "unique_id",
                "state_registration",
                "public_property_damage_type",
                "public_property_damage",
                "contributing_factor_1",
                "contributing_factor_2",
                "travel_direction",
                "vehicle_occupants",
            ],
            axis=1,
        )
