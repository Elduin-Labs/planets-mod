package com.elduin.planets.net;

import com.elduin.planets.space.SpaceTravel;

import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;

public final class ModNetworking {

	private ModNetworking() {
	}

	public static void registerServerSide() {
		PayloadTypeRegistry.playC2S().register(LaunchPayload.TYPE, LaunchPayload.CODEC);

		ServerPlayNetworking.registerGlobalReceiver(LaunchPayload.TYPE, (payload, context) ->
				context.player().server.execute(() ->
						SpaceTravel.launch(context.player(), payload.planet())));
	}
}
