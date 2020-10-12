from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.database import Repository, FetchDate, Population, PopulationTarget
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
        "district_name": str,
        "facility_name": str,
        "date": "datetime64[ns]",
        "indicator_name": str,
        "value_raw": float,
        "value_iqr": float,
        "value_std": float,
    }

    datasets = {}

    init = False

    def __init__(self, bind_string=None):
        if bind_string:
            self.engine = create_engine(bind_string)
            self.Session = sessionmaker(bind=self.engine)
            self.init = True
        assert self.init, "You must pass a DB bind string to use Database first!"
        self.__dataframe = pd.DataFrame()
        self.__districts = []
        self.__indicator_dropdown = pd.DataFrame()

    def get_session(self):
        assert (
            self.init
        ), "You must pass the bind_string into the class initialization first."
        print("Opening session")
        session = self.Session()
        return session

    @property
    def dataframe(self):

        if self.__dataframe.empty:

            self.__dataframe = pd.read_sql(self.repo_view_query, con=self.engine)

            for col in self.__dataframe.columns:
                if col in self.data_types.keys():
                    self.__dataframe[col] = self.__dataframe[col].astype(
                        self.data_types.get(col)
                    )

        return self.__dataframe

    @property
    def data_raw(self):
        return self.dataframe[
            ["district_name", "facility_name", "date", "indicator_name", "value_raw"]
        ].copy()

    @property
    def data_iqr(self):
        return self.dataframe[
            ["district_name", "facility_name", "date", "indicator_name", "value_iqr"]
        ].copy()

    @property
    def data_std(self):
        return self.dataframe[
            ["district_name", "facility_name", "date", "indicator_name", "value_std"]
        ].copy()

    @property
    def data_rep(self):
        return self.dataframe[
            ["district_name", "facility_name", "date", "indicator_name", "value_rep"]
        ].copy()

    def pivot(self, df):
        index = ["district_name", "facility_name", "date"]
        return pd.pivot_table(df, index=index, columns="indicator_name")

    @property
    def districts(self):
        if len(self.__districts) < 1:
            self.__districts = self.dataframe.district_name.unique().tolist()
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