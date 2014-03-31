package com.telenordigital.ctrlmeta.mkeep;
import com.comoyo.base.Base;
import com.comoyo.base.BaseException;

import com.comoyo.jetty.JettyServer;
import com.comoyo.jetty.JettyServer.BindingStrategy;
import com.comoyo.jetty.JettyWebAppConfig;
import com.comoyo.jetty.JettyWebAppConfig.FilterDefinition;
import com.comoyo.jetty.JettyWebAppConfig.ServletDefinition;
import com.google.common.collect.ImmutableSet;
import com.google.inject.AbstractModule;
import com.google.inject.Guice;
import com.google.inject.Injector;
import com.google.inject.servlet.GuiceFilter;
import com.google.inject.servlet.GuiceServletContextListener;
import edu.umd.cs.findbugs.annotations.SuppressWarnings;
import java.io.IOException;
import java.util.Set;
import java.util.logging.Logger;
import org.cloudname.CloudnameException;
import org.cloudname.CoordinateMissingException;
import org.eclipse.jetty.servlet.DefaultServlet;
import org.eclipse.jetty.servlet.ServletContextHandler;



/**
 * Main entry point when starting the server from the command line (which is the
 * default way of starting it). The default port on which it will start is 8012.
 *
 * @rmz
 * @paulrene
 */
@SuppressWarnings({"MS_PKGPROTECT", "MS_SHOULD_BE_FINAL"})
public final class Main {
    private static final Logger logger = Logger.getLogger(Main.class.getName());

    private static final String ENDPOINT = "james-server";
    private static final String PROTOCOL = "http";
    // This data is used by component that will make endpoint available in
    // varnish.
    private static final String ENDPOINT_DATA = "public varnish";

    /**
     * The name of this service, as we announce it to the world.
     */
    public static final String SERVICE_NAME = "James";

    protected static Set<AbstractModule> GUICE_MODULES = ImmutableSet.of();

    /**
     * Utility class, not for instantiation.
     */
    private Main() {
    }

    public static void startJamesServer(final String[] args)
            throws CloudnameException, CoordinateMissingException,
            IOException, BaseException {

        final Base base = new Base(Main.class.getPackage(), args, Config.class);

        // Register some build properties for /propz
        System.getProperties().load(
                ClassLoader.getSystemResourceAsStream("git.properties"));

        logger.info(String.format("Running %s from git sha1: %s",
                                  SERVICE_NAME, System.getProperty("git.commit.id.abbrev")));

        try {
            Config.validate();
        } catch (Exception ex) {
            base.printHelp(System.out);
            System.exit(1);
        }

        // Initialize servlet engine
        final JettyServer server = new JettyServer(
                BindingStrategy.ALL_INTERFACES, Config.PORT);

        Runtime.getRuntime().addShutdownHook(new Thread() {
            @Override
            public void run() {
                // The log system does not work in a shutdown handler.
                System.out.println("Shutting down James..");
                server.stop();
                if (Config.SHUTDOWN_SYNC) {
                    server.join(); // make sure Varnish knows we're going away
                }
                System.out.println("James has been shut down.");
                System.out.println("Shutting down Base.");
                base.shutdown();
            }
        });

        final JettyWebAppConfig webApp = new JettyWebAppConfig();

        final Injector injector = Guice.createInjector(GUICE_MODULES);

        // Add the Guice ServletContext Listener that will provide our injector.
        webApp.addEventListener(new GuiceServletContextListener() {
            @Override
            protected Injector getInjector() {
                return injector;
            }
        });

        // Add the Guice Filter for all paths.
        FilterDefinition guiceFilterDefinition = new FilterDefinition(new GuiceFilter(), "/*");
        webApp.addFilterDefinition(guiceFilterDefinition);

        DefaultServlet defaultServlet = new DefaultServlet();
        ServletDefinition defaultServletDefinition = new ServletDefinition(defaultServlet, "/*");
        webApp.addServletDefinition(defaultServletDefinition);

        // Register the application configuration.
        server.addWebApplication("/", webApp,
                ServletContextHandler.SESSIONS | ServletContextHandler.NO_SECURITY);

        logger.info(String.format("Starting %s server on port %d ( http://0.0.0.0:%d ) ",
                                  SERVICE_NAME, Config.PORT, Config.PORT));
        server.start();
        base.publishEndpoint(ENDPOINT, PROTOCOL, ENDPOINT_DATA, Config.PORT);
    }

    /**
     * Main entry point.
     *
     * @param args
     *            Command line.
     * @throws Exception
     *             if something goes wrong.
     */
    public static void main(final String[] args) throws Exception {
        startJamesServer(args);
    }
}
