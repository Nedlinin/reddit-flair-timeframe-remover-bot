import configparser
import os


class _ConfigBase:
    # We don't want to accidentally add anything to this config.
    # This allows us to throw and error in the __new__ call above if a programmer makes a typo.
    # For instance, using cls._instance.REDDIT_CLIENT_SECRET rather than cls._instance.REDDIT.CLIENT_SECRET
    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise TypeError(
                "{} is a frozen class.  You cannot dynamically add properties.  Property attempted: {}, value: {}".format(
                    self, key, value))

    # Ensure every config value is properly set.
    # Note: This would currently fail on falsey values like 0.
    def is_valid(self) -> bool:
        for key, value in vars(self).items():
            if not value:
                return False

        return True


class Config(_ConfigBase):
    _instance = None

    # Note: You must specify a default value.  The value of None is fine.
    class _REDDIT(_ConfigBase):
        CLIENT_ID: str = ""
        CLIENT_SECRET: str = ""
        USER_NAME: str = ""
        PASSWORD: str = ""
        SUBREDDIT: str = ""
        USER_AGENT: str = "Remove Posts by Flair Bot"
        DAY_START: str = ""
        DAY_END: str = ""
        FLAIR_TO_REMOVE: str = ""
        REMOVAL_REASON_ID: str = ""

    REDDIT: _REDDIT = _REDDIT()

    def is_valid(self) -> bool:
        # If we ever expand to multiple classes holding config we simply and them together.
        return self.REDDIT.is_valid()

    # Ensure singleton so we aren"t reading the config over and over for each service using it.
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            config = configparser.ConfigParser(strict=False, interpolation=None)

            try:
                config.read("{}/config/config.ini".format(os.path.dirname(os.path.realpath(__file__))))
                cls._instance.REDDIT.CLIENT_ID = config.get("REDDIT", "CLIENT_ID")
                cls._instance.REDDIT.CLIENT_SECRET = config.get("REDDIT", "CLIENT_SECRET")
                cls._instance.REDDIT.PASSWORD = config.get("REDDIT", "PASSWORD")
                cls._instance.REDDIT.USER_NAME = config.get("REDDIT", "USER_NAME")
                cls._instance.REDDIT.SUBREDDIT = config.get("REDDIT", "SUBREDDIT")
                cls._instance.REDDIT.USER_AGENT = config.get("REDDIT", "USER_AGENT")
                cls._instance.REDDIT.DAY_START = config.get("REDDIT", "DAY_START")
                cls._instance.REDDIT.DAY_END = config.get("REDDIT", "DAY_END")
                cls._instance.REDDIT.FLAIR_TO_REMOVE = config.get("REDDIT", "FLAIR_TO_REMOVE")
                cls._instance.REDDIT.REMOVAL_REASON_ID = config.get("REDDIT", "REMOVAL_REASON_ID")

                # Ensure all configuration appears valid.
                if not cls._instance.is_valid():
                    exit("Some config properties on not properly set.")

            except TypeError as e:
                print(e)
                exit("Additional field detected on config class.  Please add this in the proper way.")
            except Exception:
                exit("Please make sure config/config.ini is set.")

        return cls._instance
