package com.elduin.planets.client;

import com.elduin.planets.Planet;
import com.elduin.planets.net.LaunchPayload;

import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.CommonComponents;
import net.minecraft.network.chat.Component;

/** The little mission control panel you get when you right-click a rocket. */
public class LaunchScreen extends Screen {

	private static final int BUTTON_WIDTH = 190;
	private static final int BUTTON_HEIGHT = 20;

	private Planet hovered;

	public LaunchScreen() {
		super(Component.translatable("planets.screen.title"));
	}

	@Override
	protected void init() {
		Planet here = currentPlanet();
		int y = this.height / 2 - 66;

		for (Planet planet : Planet.values()) {
			Component label = planet == here
					? Component.translatable("planets.screen.here")
					.append(": ").append(Component.translatable(planet.nameKey()))
					: Component.translatable(planet.nameKey());

			Button button = Button.builder(label, pressed -> choose(planet))
					.bounds(this.width / 2 - BUTTON_WIDTH / 2, y, BUTTON_WIDTH, BUTTON_HEIGHT)
					.build();
			button.active = planet != here;
			this.addRenderableWidget(button);
			y += BUTTON_HEIGHT + 4;
		}

		this.addRenderableWidget(Button.builder(CommonComponents.GUI_CANCEL, pressed -> this.onClose())
				.bounds(this.width / 2 - 60, y + 12, 120, BUTTON_HEIGHT)
				.build());
	}

	private void choose(Planet planet) {
		ClientPlayNetworking.send(new LaunchPayload(planet.ordinal()));
		this.onClose();
	}

	private static Planet currentPlanet() {
		Minecraft mc = Minecraft.getInstance();
		return mc.player == null ? null : Planet.of(mc.player.level().dimension());
	}

	@Override
	public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
		super.render(graphics, mouseX, mouseY, partialTick);

		graphics.drawCenteredString(this.font, this.title, this.width / 2, this.height / 2 - 90, 0xFFFFFF);

		// Whichever planet the mouse is over gets a line of description at the bottom.
		hovered = planetUnder(mouseY);
		if (hovered != null) {
			graphics.drawCenteredString(this.font, Component.translatable(hovered.blurbKey()),
					this.width / 2, this.height / 2 + 62, 0xA0C8FF);
			graphics.drawCenteredString(this.font,
					Component.translatable("planets.screen.gravity", hovered.gravityText()),
					this.width / 2, this.height / 2 + 74, 0x8899AA);
		}
	}

	private Planet planetUnder(int mouseY) {
		int top = this.height / 2 - 66;
		int index = (mouseY - top) / (BUTTON_HEIGHT + 4);
		if (mouseY < top || index < 0 || index >= Planet.values().length) {
			return null;
		}
		return Planet.values()[index];
	}

	@Override
	public boolean isPauseScreen() {
		return false;
	}
}
