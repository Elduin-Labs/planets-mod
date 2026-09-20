package com.elduin.planets.space;

import com.elduin.planets.Planet;
import com.elduin.planets.registry.ModBlocks;

import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;

/** Getting off the ground, and putting you down somewhere you can stand. */
public final class SpaceTravel {

	/** How far the rocket can be and still count as "you are in the rocket". */
	private static final int ROCKET_RANGE = 8;

	private SpaceTravel() {
	}

	public static void launch(ServerPlayer player, int planetIndex) {
		Planet target = Planet.byIndex(planetIndex);
		if (target == null || target == Planet.of(player.level().dimension())) {
			return;
		}

		if (!nearRocket(player)) {
			player.displayClientMessage(Component.translatable("planets.message.no_rocket"), true);
			return;
		}

		ServerLevel destination = player.server.getLevel(target.dimension());
		if (destination == null) {
			return;
		}

		player.level().playSound(null, player.blockPosition(), SoundEvents.FIREWORK_ROCKET_LAUNCH,
				SoundSource.PLAYERS, 2.0F, 0.6F);

		BlockPos landing = findLanding(destination, player.blockPosition());
		if (target != Planet.EARTH) {
			buildLandingPad(destination, landing);
		}

		teleport(player, destination, landing);

		destination.playSound(null, landing, SoundEvents.FIREWORK_ROCKET_BLAST,
				SoundSource.PLAYERS, 2.0F, 0.8F);
		player.displayClientMessage(
				Component.translatable("planets.message.arrived", Component.translatable(target.nameKey())),
				false);
	}

	/** You have to be standing by a rocket, so you can't just wish yourself to Mars. */
	private static boolean nearRocket(ServerPlayer player) {
		BlockPos at = player.blockPosition();
		for (BlockPos pos : BlockPos.betweenClosed(
				at.offset(-ROCKET_RANGE, -ROCKET_RANGE, -ROCKET_RANGE),
				at.offset(ROCKET_RANGE, ROCKET_RANGE, ROCKET_RANGE))) {
			if (player.level().getBlockState(pos).is(ModBlocks.ROCKET)) {
				return true;
			}
		}
		return false;
	}

	/** First air above the ground, at the same x/z you left from. */
	private static BlockPos findLanding(ServerLevel level, BlockPos from) {
		int x = from.getX();
		int z = from.getZ();
		// Force the chunk to generate, otherwise the heightmap is all zeroes.
		level.getChunk(x >> 4, z >> 4);
		int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
		if (y <= level.dimensionType().minY() + 1) {
			y = 96;
		}
		return new BlockPos(x, y + 1, z);
	}

	/** A 5x5 pad so you don't land in a hole, and a rocket so you can always get home. */
	private static void buildLandingPad(ServerLevel level, BlockPos landing) {
		BlockState pad = padBlock(level);
		BlockPos floor = landing.below();
		for (int dx = -2; dx <= 2; dx++) {
			for (int dz = -2; dz <= 2; dz++) {
				level.setBlockAndUpdate(floor.offset(dx, 0, dz), pad);
				for (int dy = 0; dy < 3; dy++) {
					BlockPos clear = landing.offset(dx, dy, dz);
					if (!level.getBlockState(clear).isAir()) {
						level.setBlockAndUpdate(clear, Blocks.AIR.defaultBlockState());
					}
				}
			}
		}
		level.setBlockAndUpdate(landing.offset(2, 0, 0), ModBlocks.ROCKET.defaultBlockState());
	}

	private static BlockState padBlock(ServerLevel level) {
		Planet planet = Planet.of(level.dimension());
		if (planet == null) {
			return Blocks.SMOOTH_STONE.defaultBlockState();
		}
		return switch (planet) {
			case MOON -> ModBlocks.MOON_ROCK.defaultBlockState();
			case MARS -> ModBlocks.MARS_ROCK.defaultBlockState();
			case VENUS -> ModBlocks.VENUS_ROCK.defaultBlockState();
			case PLUTO -> ModBlocks.PLUTO_ICE.defaultBlockState();
			default -> Blocks.SMOOTH_STONE.defaultBlockState();
		};
	}

	private static void teleport(ServerPlayer player, ServerLevel destination, BlockPos landing) {
		double x = landing.getX() + 0.5;
		double y = landing.getY();
		double z = landing.getZ() + 0.5;
		player.fallDistance = 0.0F;
		//? if 1.21.1 {
		/*player.teleportTo(destination, x, y, z, player.getYRot(), player.getXRot());
		*///? } else {
		player.teleportTo(destination, x, y, z, java.util.Set.of(), player.getYRot(), player.getXRot(), true);
		//? }
	}
}
