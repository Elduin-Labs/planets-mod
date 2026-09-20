package com.elduin.planets.client;

import net.fabricmc.fabric.api.client.screen.v1.ScreenEvents;
import net.fabricmc.fabric.api.client.screen.v1.Screens;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.client.gui.screens.worldselection.CreateWorldScreen;
import net.minecraft.client.gui.screens.worldselection.WorldCreationUiState;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.levelgen.FlatLevelSource;
import net.minecraft.world.level.levelgen.flat.FlatLevelGeneratorPresets;
import net.minecraft.world.level.levelgen.flat.FlatLevelGeneratorSettings;
import net.minecraft.world.level.levelgen.presets.WorldPresets;

/**
 * A "Create Test World" button on the title screen. It opens the normal world
 * creation screen with Superflat already picked and the Redstone Ready preset
 * already loaded, so a flat world for trying things out is two clicks away.
 */
public final class TestWorldButton {

	/**
	 * Set when the button is pressed, cleared once the create-world screen has
	 * been set up. Opening that screen loads a whole datapack context first, so
	 * we can't rely on it existing the moment the button is clicked — we wait
	 * for the screen to initialise and configure it then.
	 */
	private static boolean pending;

	private TestWorldButton() {
	}

	public static void register() {
		ScreenEvents.AFTER_INIT.register((client, screen, width, height) -> {
			if (screen instanceof TitleScreen) {
				addButton(client, screen, height);
			} else if (screen instanceof CreateWorldScreen create && pending) {
				pending = false;
				setUpTestWorld(create);
			}
		});
	}

	private static void addButton(Minecraft client, Screen parent, int height) {
		Button button = Button.builder(Component.translatable("planets.button.test_world"), pressed -> {
					pending = true;
					CreateWorldScreen.openFresh(client, parent);
				})
				.bounds(4, height - 46, 130, 20)
				.tooltip(Tooltip.create(Component.translatable("planets.button.test_world.tooltip")))
				.build();
		Screens.getButtons(parent).add(button);
	}

	private static void setUpTestWorld(CreateWorldScreen screen) {
		WorldCreationUiState state = screen.getUiState();
		state.setName("Planets Test");
		selectSuperflat(state);
		applyRedstoneReady(state);
	}

	private static void selectSuperflat(WorldCreationUiState state) {
		for (WorldCreationUiState.WorldTypeEntry entry : state.getNormalPresetList()) {
			if (entry.preset().is(WorldPresets.FLAT)) {
				state.setWorldType(entry);
				return;
			}
		}
	}

	private static void applyRedstoneReady(WorldCreationUiState state) {
		RegistryAccess.Frozen registries = state.getSettings().worldgenLoadContext();
		FlatLevelGeneratorSettings flat = registries
				.lookupOrThrow(Registries.FLAT_LEVEL_GENERATOR_PRESET)
				.getOrThrow(FlatLevelGeneratorPresets.REDSTONE_READY)
				.value()
				.settings();
		state.updateDimensions((frozen, dimensions) ->
				dimensions.replaceOverworldGenerator(frozen, new FlatLevelSource(flat)));
	}
}
