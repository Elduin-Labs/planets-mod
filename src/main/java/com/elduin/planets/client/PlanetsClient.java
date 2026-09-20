package com.elduin.planets.client;

import com.elduin.planets.Hooks;

import net.minecraft.client.Minecraft;

public final class PlanetsClient {

	private PlanetsClient() {
	}

	public static void init() {
		Hooks.openLaunchScreen = () -> Minecraft.getInstance().setScreen(new LaunchScreen());
	}
}
