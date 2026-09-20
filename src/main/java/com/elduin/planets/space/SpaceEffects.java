package com.elduin.planets.space;

import com.elduin.planets.Planet;
import com.elduin.planets.PlanetsMod;
import com.elduin.planets.registry.ModItems;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageType;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;

/**
 * What being on another planet actually feels like: you weigh less, and there
 * is nothing to breathe unless you brought some.
 */
public final class SpaceEffects {

	private static final ResourceLocation GRAVITY_MODIFIER = PlanetsMod.id("planet_gravity");
	private static final ResourceLocation FALL_MODIFIER = PlanetsMod.id("planet_soft_landing");

	private static final ResourceKey<DamageType> VACUUM =
			ResourceKey.create(Registries.DAMAGE_TYPE, PlanetsMod.id("vacuum"));

	/** Half a heart every two seconds, so there's time to get back in the rocket. */
	private static final int AIR_CHECK_TICKS = 40;

	private SpaceEffects() {
	}

	public static void register() {
		ServerTickEvents.END_SERVER_TICK.register(server -> {
			if (server.getTickCount() % 20 != 0) {
				return;
			}
			for (ServerPlayer player : server.getPlayerList().getPlayers()) {
				Planet planet = Planet.of(player.level().dimension());
				applyGravity(player, planet);
				if (planet != null && !planet.breathable()
						&& server.getTickCount() % AIR_CHECK_TICKS == 0) {
					checkAir(player);
				}
			}
		});
	}

	private static void applyGravity(ServerPlayer player, Planet planet) {
		AttributeInstance gravity = player.getAttribute(Attributes.GRAVITY);
		AttributeInstance fall = player.getAttribute(Attributes.SAFE_FALL_DISTANCE);

		if (gravity != null) {
			gravity.removeModifier(GRAVITY_MODIFIER);
			if (planet != null && planet.gravity() != 1.0) {
				gravity.addTransientModifier(new AttributeModifier(GRAVITY_MODIFIER,
						planet.gravity() - 1.0, AttributeModifier.Operation.ADD_MULTIPLIED_BASE));
			}
		}

		// Falling slowly should not still break your legs.
		if (fall != null) {
			fall.removeModifier(FALL_MODIFIER);
			if (planet != null && planet.gravity() < 1.0) {
				fall.addTransientModifier(new AttributeModifier(FALL_MODIFIER,
						12.0, AttributeModifier.Operation.ADD_VALUE));
			}
		}
	}

	private static void checkAir(ServerPlayer player) {
		if (player.isCreative() || player.isSpectator() || hasOxygen(player)) {
			return;
		}
		player.displayClientMessage(Component.translatable("planets.message.no_oxygen"), true);
		player.hurt(vacuum(player), 1.0F);
	}

	private static boolean hasOxygen(ServerPlayer player) {
		for (int slot = 0; slot < player.getInventory().getContainerSize(); slot++) {
			if (player.getInventory().getItem(slot).is(ModItems.OXYGEN_TANK)) {
				return true;
			}
		}
		return false;
	}

	private static DamageSource vacuum(ServerPlayer player) {
		//? if 1.21.1 {
		return new DamageSource(player.level().registryAccess()
				.registryOrThrow(Registries.DAMAGE_TYPE).getHolderOrThrow(VACUUM));
		//? } else {
		/*return new DamageSource(player.level().registryAccess()
				.lookupOrThrow(Registries.DAMAGE_TYPE).getOrThrow(VACUUM));
		*///? }
	}
}
