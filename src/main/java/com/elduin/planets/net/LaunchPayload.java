package com.elduin.planets.net;

import com.elduin.planets.PlanetsMod;

import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;

/** Client -> server: "send me to the planet at this position in the list". */
public record LaunchPayload(int planet) implements CustomPacketPayload {

	public static final CustomPacketPayload.Type<LaunchPayload> TYPE =
			new CustomPacketPayload.Type<>(PlanetsMod.id("launch"));

	public static final StreamCodec<RegistryFriendlyByteBuf, LaunchPayload> CODEC =
			StreamCodec.composite(ByteBufCodecs.VAR_INT, LaunchPayload::planet, LaunchPayload::new);

	@Override
	public CustomPacketPayload.Type<? extends CustomPacketPayload> type() {
		return TYPE;
	}
}
