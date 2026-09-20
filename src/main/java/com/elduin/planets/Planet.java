package com.elduin.planets;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;

/**
 * Everywhere you can fly to. Earth is first so it is always the way home.
 *
 * <p>{@code gravity} is a multiple of Earth's. 1.0 is normal, 0.17 is the real
 * Moon, and anything under about 0.1 means you go up and stay up for a while.
 */
public enum Planet {

	EARTH("overworld", Level.OVERWORLD, 1.00, true),
	MOON("moon", dimension("moon"), 0.17, false),
	MARS("mars", dimension("mars"), 0.38, false),
	VENUS("venus", dimension("venus"), 0.90, false),
	PLUTO("pluto", dimension("pluto"), 0.06, false);

	private final String id;
	private final ResourceKey<Level> dimension;
	private final double gravity;
	private final boolean breathable;

	Planet(String id, ResourceKey<Level> dimension, double gravity, boolean breathable) {
		this.id = id;
		this.dimension = dimension;
		this.gravity = gravity;
		this.breathable = breathable;
	}

	private static ResourceKey<Level> dimension(String name) {
		return ResourceKey.create(Registries.DIMENSION, PlanetsMod.id(name));
	}

	public String id() {
		return id;
	}

	public ResourceKey<Level> dimension() {
		return dimension;
	}

	public double gravity() {
		return gravity;
	}

	public boolean breathable() {
		return breathable;
	}

	public String nameKey() {
		return "planets.planet." + id;
	}

	public String blurbKey() {
		return "planets.blurb." + id;
	}

	/** How the gravity reads on the launch screen: "17% of Earth". */
	public String gravityText() {
		return Math.round(gravity * 100) + "%";
	}

	public static Planet byIndex(int index) {
		Planet[] all = values();
		return index >= 0 && index < all.length ? all[index] : null;
	}

	/** The planet a dimension belongs to, or null for somewhere we don't know. */
	public static Planet of(ResourceKey<Level> dimension) {
		for (Planet planet : values()) {
			if (planet.dimension.equals(dimension)) {
				return planet;
			}
		}
		return null;
	}
}
