from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.database import Repository, FetchDate, Population, PopulationTarget, District
import pandas as pd


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """
    Singleton database class
    ! This class should be called for the first time with DB bind_string.

    Keyword arguments:
    bind_string -- SQLAlchemy-like DB bind string
    Return: Database
    """

    repo_view_query = """SELECT * FROM dataset;"""
    dropdown_query = """SELECT * FROM dropdown_indicator;"""

    data_types = {
        # "district_name": str,
        # "facility_name": str,
        "date": "datetime64[ns]",
        # "indicator_name": str,
        # "value_raw": float,
        # "value_iqr": float,
        # "value_std": float,
        # "value_rep": int
    }

    index_columns = ["id", "facility_name", "date", "year", "month"]

    datasets = {}
    raw_data = {}

    init = False

    def __init__(self, bind_string=None):
        if bind_string:
            self.engine = create_engine(bind_string)
            self.Session = sessionmaker(bind=self.engine)

            print("Fetching data")
            repo_data = self.get_repository()  # VERY COSTLY, USE WITH CARE
            print("Setting districts")
            self.__districts = repo_data.id.unique().tolist()
            self.__districts.sort()
            print("Pivoting data")
            for val_col in ["value_raw", "value_std", "value_iqr", "value_rep"]:
                df = self.pivot_df(repo_data, val_col)
                self.raw_data[val_col] = df

            self.init = True

        assert self.init, "You must pass a DB bind string to use Database first!"
        self.__indicator_dropdown = pd.DataFrame()

    def get_session(self):
        assert (
            self.init
        ), "You must pass the bind_string into the class initialization first."
        print("Opening session")
        session = self.Session()
        return session

    def get_repository(self):

        __dataframe = pd.read_sql(self.repo_view_query, con=self.engine)

        for col in __dataframe.columns:
            if col in self.data_types.keys():
                print(f"Convering {col}")
                __dataframe[col] = __dataframe[col].astype(self.data_types.get(col))

        year = []
        month = []
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]

        for date in __dataframe.date:
            year.append(date.year)
            month.append(months[date.month - 1])

        __dataframe["year"] = year

        __dataframe["month"] = month

        __dataframe.rename(columns={"district_name": "id"}, inplace=True)

        return __dataframe

    def pivot_df(self, df, value_column):
        out = df.reset_index()
        out = out[self.index_columns + ["indicator_name", value_column]]
        out = pd.pivot_table(
            out, index=self.index_columns, columns="indicator_name", aggfunc="first"
        )
        out.columns = out.columns.droplevel(0)
        out = out.reset_index()
        return out

    @property
    def districts(self):
        return self.__districts

    @property
    def indicator_dropdowns(self):
        if self.__indicator_dropdown.empty:
            self.__indicator_dropdown = pd.read_sql(self.dropdown_query, self.engine)
        return self.__indicator_dropdown

    @property
    def fetch_date(self):
        session = self.Session()
        date = session.query(FetchDate).one()
        session.close()
        return date.serialize()

    def filter_by_indicator(self, df, indicator):
        df = df.reset_index()
        try:
            df = df[self.index_columns + [indicator]]
            # df = df.set_index(self.index_columns)
        except Exception as e:
            print(e)
            print("No such column is present in the dataframe")
        return df

    # !TODO basic error handling
    def include_dataset(self, key, df):
        self.datasets[key] = df

    def fetch_dataset(self, key):
        return self.datasets.get(key)

    def get_serialized_into_df(self, sqlalchemy_obj):
        session = self.Session()
        objects = session.query(sqlalchemy_obj).all()
        df = pd.DataFrame([obj.serialize() for obj in objects])
        return df

    def get_population_data(self):
        return self.get_serialized_into_df(Population)

    def get_population_target(self):
        return self.get_serialized_into_df(PopulationTarget)

    def filter_by_policy(self, policy):
        dropdown_filters = {
            "Correct outliers - using standard deviation": "value_std",
            "Correct outliers - using interquartile range": "value_iqr",
            "Keep outliers": "value_raw",
            "Reporting": "value_rep",
        }
        return self.raw_data.get(dropdown_filters.get(policy)).copy()
