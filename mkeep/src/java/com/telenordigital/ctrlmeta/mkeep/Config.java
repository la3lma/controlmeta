package com.telenordigital.ctrlmeta.mkeep;

import com.google.common.collect.ImmutableMap;

import java.util.Locale;

import org.cloudname.flags.Flag;

/**
 * Manages all of the flags passed into James as command line arguments.
 */
public class Config {
    /**
     * The highest legal IP port number.
     */
    private static final int MAX_IP_PORT_NUMBER = 65535;

    public static final int SECONDS_IN_AN_HOUR = 3600;

    public static final String DEFAULT_MARKET = "no";

    public static final String CONFIG_SEPARATOR = ",";

    @Flag(name = ConfigNames.PORT, description = "server port")
    public static int PORT = 8012;

    @Flag(name = ConfigNames.USERNAME, description = "An username to use when accessing the service")
    public static String USERNAME = "";

    @Flag(name = ConfigNames.PASSWORD, description = "A password to use when accessing the service")
    public static String PASSWORD = "";

    @Flag(name = ConfigNames.MONGO_PLAYERSTATE_DB,
            description = "The mongo database used to store player state (for single stream restrictions)")
    public static String MONGO_PLAYERSTATE_DB = "james-playerstate";

    @Flag(name = ConfigNames.MONGO_PLAYERSTATE_COLLECTION,
            description = "The mongo collection used to store player state (for single stream restrictions)")
    public static String MONGO_PLAYERSTATE_COLLECTION = "state";

    @Flag(name = ConfigNames.MONGO_LISTS_DB, description = "Name of database in mongo to use for favorite lists")
    public static String MONGO_LISTS_DB = "james-lists";

    @Flag(name = ConfigNames.MONGO_USER_DB, description = "Name of database in mongo to use for resume and history api")
    public static String MONGO_USER_DB = "james-user-db";

    @Flag(name = ConfigNames.MONGO_URI, description = "uri to mongo instance")
    public static String MONGO_URI = "mongodb://127.0.0.1:27017";

    @Flag(name = ConfigNames.TICKET_SECRET, description = "The secret to be used for signing tickets. Must be usable input for HmacSHA1.")
    public static String TICKET_SECRET = "DEADBEEF";

    /* S3 configuration parameters */
    @Flag(name = ConfigNames.AWS_ACCESS_KEY,
          description = "The AWS Credentials access key for your user")
    public static String AWS_ACCESS_KEY = "";

    @Flag(name = ConfigNames.AWS_SECRET_KEY,
          description = "The AWS Credentials secret key for your user")
    public static String AWS_SECRET_KEY = "";

    @Flag(name = ConfigNames.AWS_S3_ENDPOINT, description = "The s3 region endpoint")
    public static String AWS_S3_ENDPOINT = "s3-eu-west-1.amazonaws.com";

    @Flag(name = ConfigNames.AWS_S3_METAMINDER_BUCKET_NAME,
          description = "The bucket name for metaminder data")
    public static String AWS_S3_METAMINDER_BUCKET_NAME = "metaminder-staging.comoyo.com";

    @Flag(name = ConfigNames.AWS_S3_PUBLISHER_BUCKET_NAME,
          description = "The bucket name for publisher data")
    public static String AWS_S3_PUBLISHER_BUCKET_NAME = "publisher-staging.comoyo.com";

    @Flag(name = ConfigNames.METAMINDER_DATA_URL,
            description = "The url for a directory path, which contains "
            + " latest.metadminder-film(episode|series|season|person) file used to retrieve "
            + " metaminder content.")
    public static String METAMINDER_DATA_URL = "";

    @Flag(name = ConfigNames.PUBLISHER_DATA_URL,
            description = "The url for a directory path, which contains a "
            + "latest.publisher-assetitem file used to retrieve publisher content.")
    public static String PUBLISHER_DATA_URL = "";

    @Flag(name = ConfigNames.CACHE_REFRESH_INTERVAL,
            description = "Interval in seconds for how often to reload the content cache")
    protected static int CACHE_REFRESH_INTERVAL = SECONDS_IN_AN_HOUR;

    @Flag(name = ConfigNames.SUPER_USERS,
            description = "A comma separated list of super users of the system.")
    public static String SUPER_USERS = "front";

    @Flag(name = ConfigNames.DEVELOPERS,
            description = "A comman separated list of users which get developer privileges.")
    public static String DEVELOPERS = "";

    @Flag(name = ConfigNames.MARKETS,
            description = "A comma separated list of 2 letters country code per market")
    public static String MARKETS = "no,se,dk";

    @Flag(name = ConfigNames.BOOTSTRAPPED_LISTS,
            description = "A comma separated list of bootstrapped lists")
    public static String BOOTSTRAPPED_LISTS = "content/welcome,content/film,content/series"
            + ",content/children,content/provider";

    @Flag(name = ConfigNames.OAUTH_API_URL, description = "Url for the oauth service")
    public static String OAUTH_API_URL = "https://stagingapi.c.skunk-works.no/oauth/tokeninfo";

    @Flag(name = ConfigNames.OAUTH_API_CLIENTID, description = "Client id for the oauth service")
    public static String OAUTH_API_CLIENTID = "comoyo-svod-service";

    @Flag(name = ConfigNames.OAUTH_API_SECRET, description = "Api secret for the oauth service")
    public static String OAUTH_API_SECRET = "taken-thrones-godfather-hobbit-taxi";

    @Flag(name = ConfigNames.OAUTH_CACHE_EXPIRE_TIME,
            description = "Time in seconds that oauth responses are cached. 0 = disable caching")
    public static int OAUTH_CACHE_DURATION = 0;

    @Flag(name = ConfigNames.OAUTH_CACHE_REFRESH_TIME,
            description = "Time in seconds that oauth responses are considered valid, before a" +
            " background refresh is scheduled.")
    public static int OAUTH_CACHE_REFRESH_TIME = 1;

    @Flag(name = ConfigNames.CONTENT_PROVIDER_LISTS,
            description = "A comma separated list of content providers")
    public static String CONTENT_PROVIDER_LISTS = "cmore";

    @Flag(name = ConfigNames.SYLFIDE_API_CLIENTID)
    public static String SYLFIDE_API_CLIENTID = "james";

    @Flag(name = ConfigNames.SYLFIDE_API_SECRET)
    public static String SYLFIDE_API_SECRET = "james";

    @Flag(name = ConfigNames.SYLFIDE_API_URL)
    public static String SYLFIDE_API_URL = "https://stagingapi.comoyo.com/id";

    @Flag(name = ConfigNames.SYLFIDE_CACHE_EXPIRE_TIME,
            description = "Time in seconds that sylfide responses are cached. 0 = disable caching")
    public static int SYLFIDE_CACHE_DURATION = 0;

    @Flag(name = ConfigNames.SYLFIDE_CACHE_REFRESH_TIME,
            description = "Time in seconds that sylfide responses are considered valid, before a" +
            " background refresh is scheduled.")
    public static int SYLFIDE_CACHE_REFRESH_TIME = 1;

    @Flag(name = ConfigNames.MINIMUM_LISTS_SIZE,
            description = "Lists of links with less items than this threshold will be filtered out.")
    public static int MINIMUM_LISTS_SIZE = 0;

    @Flag(name = ConfigNames.SHUTDOWN_SYNC,
            description = "Boolean that specifies if james should sync with Base when shutting down.")
    public static boolean SHUTDOWN_SYNC = true;

    @Flag(name = ConfigNames.GEOLOCATION_API_URL,
            description = "URL of the Comoyo Geolocation API")
    public static String GEOLOCATION_API_URL = "https://stagingapi.comoyo.com/geolocation/lookup";

    @Flag(name = ConfigNames.DISABLE_GEOLOCATION,
            description = "Boolean that specifies if james should omit all geolocation.")
    public static boolean DISABLE_GEOLOCATION = false;

    @Flag(name = ConfigNames.MAX_CONCURRENT_DEVICES,
            description = "Maximum number of devices that may be activated concurrently per user.")
    public static int MAX_CONCURRENT_DEVICES = 4;

    private static final ImmutableMap<String, Locale> MARKET_TO_LOCALES =
            ImmutableMap.of("no", new Locale("no", "NO"),
                            "se", new Locale("sv", "SE"),
                            "dk", new Locale("da", "DK"));

    public static void validate() throws NullPointerException, IllegalArgumentException {
        // Username/password
        checkNotNull(USERNAME, "Username can't be null");
        checkNotNull(PASSWORD, "Password can't be null");

        checkArgument(!USERNAME.trim().isEmpty(), "Username can't be empty");
        checkArgument(!PASSWORD.trim().isEmpty(), "Password can't be empty");

        checkArgument(PORT > 0);
        checkArgument(PORT < MAX_IP_PORT_NUMBER);
    }

    /**
     * Get a reasonable locale for the specified market.
     */
    public static Locale defaultLocaleForMarket(final String market) {
        return MARKET_TO_LOCALES.get(market);
    }

    /**
     * Get a canonical string representation of the Locale object
     */
    public static String localeString(final Locale locale) {
        return String.format("%s-%s", locale.getLanguage(), locale.getCountry());
    }
}
