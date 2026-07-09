import Link from "next/link";

export default function CancelPage() {
  return (
    <section className="panel payment-status">
      <h2>Checkout canceled</h2>
      <p>Your worksheet was not charged. You can return and try again when you are ready.</p>
      <div className="payment-actions">
        <Link className="secondary button-link" href="/">
          Back to worksheet
        </Link>
      </div>
    </section>
  );
}
