import click
from .core.engine import TriadicEngine


@click.group()
def main():
    """Triadix CLI."""
    pass


@main.command()
@click.option("--blocks", default=96, show_default=True, help="Number of blocks")
def run(blocks: int):
    click.echo("Starting Triadix...")
    engine = TriadicEngine()
    chain = engine.run(blocks=blocks)
    stats = engine.coherence_stats()

    click.echo(f"Done. {len(chain)} blocks generated.")
    click.echo(f"Valid: {'Yes' if engine.is_chain_valid() else 'No'}")
    click.echo(f"Healthy: {'Yes' if engine.is_healthy() else 'No'}")
    click.echo(f"Tau: {engine.config.tau:.6f}")
    click.echo(f"Health mode: {engine.config.health_mode}")
    click.echo(f"C range: {stats['min']:.6f} - {stats['max']:.6f}")
    click.echo(f"C p05/p50/p95: {stats['p05']:.6f} / {stats['p50']:.6f} / {stats['p95']:.6f}")
    click.echo(f"Fraction >= tau: {stats['fraction_ge_tau']:.6f}")
    click.echo(f"Output: {engine.config.run_root}")


@main.command()
@click.option("--blocks", default=96, show_default=True, help="Number of blocks")
def validate(blocks: int):
    engine = TriadicEngine()
    engine.run(blocks=blocks)
    click.echo("Chain valid." if engine.is_chain_valid() else "Chain invalid.")
    click.echo("Chain healthy." if engine.is_healthy() else "Chain not healthy.")


if __name__ == "__main__":
    main()