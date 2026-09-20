package com.elduin.planets.platform.fabric.datagen;

//? fabric {
import net.fabricmc.fabric.api.datagen.v1.DataGeneratorEntrypoint;
import net.fabricmc.fabric.api.datagen.v1.FabricDataGenerator;

/**
 * Planets writes its data pack by hand, because 1.21.1 and 1.21.4 disagree
 * about what half the folders are called. Nothing is generated here, but the
 * class has to exist: the build names it in the mod manifest.
 */
public class FabricDataGeneratorEntrypoint implements DataGeneratorEntrypoint {

	@Override
	public void onInitializeDataGenerator(FabricDataGenerator generator) {
	}

}
//?}
