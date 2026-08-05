import Link from "next/link";

export default function CancelPage() {
  return (
    <section className="panel payment-status">
      <h2>Checkout canceled</h2>
      <p>No charge was made. You can return and pay once or subscribe when you are ready.</p>
      <div className="payment-actions">
        <Link className="secondary button-link" href="/">
          Back to worksheet
        </Link>
      </div>
    </section>
  );
}
