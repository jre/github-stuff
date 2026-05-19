import java.io.FileInputStream
import java.util.Properties

val keystoreProps = Properties()
rootProject.file("keystore.properties").let { ks ->
    if (ks.canRead())
        keystoreProps.load(FileInputStream(ks))
}

android {
    signingConfigs {
        register("config") {
            storeFile = keystoreProps.getProperty("storeFile")?.let {file(it)}
            storePassword = keystoreProps.getProperty("storePassword")
            keyPassword = keystoreProps.getProperty("keyPassword")
            keyAlias = keystoreProps.getProperty("keyAlias")
        }
    }
    buildTypes {
        getByName("debug") {
            if (signingConfigs["config"].storeFile != null)
                signingConfig = signingConfigs["config"]
        }
        getByName("release") {
            signingConfig = signingConfigs["config"]
        }
    }
}
