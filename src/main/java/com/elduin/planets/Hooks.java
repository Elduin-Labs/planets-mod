package com.elduin.planets;

/**
 * A tiny hand-off between shared code and client-only code.
 *
 * <p>A dedicated server never loads the launch screen class, so shared classes
 * must not mention it by name. The client entrypoint fills this in on startup;
 * on a server it stays a no-op.
 */
public final class Hooks {

	public static Runnable openLaunchScreen = () -> {
	};

	private Hooks() {
	}
}
