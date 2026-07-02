export default function TypingIndicator() {
  return (
    <div className="flex items-start gap-3 px-4 py-3 animate-fade-in">
      <div className="w-7 h-7 rounded-full bg-accent/20 flex items-center justify-center shrink-0 mt-0.5">
        <span className="text-accent text-xs font-bold">IF</span>
      </div>
      <div className="flex items-center gap-1 pt-2">
        {[0, 1, 2].map(i => (
          <span
            key={i}
            className="w-1.5 h-1.5 rounded-full bg-text-muted"
            style={{ animation: `pulseDot 1.4s ease-in-out ${i * 0.16}s infinite` }}
          />
        ))}
      </div>
    </div>
  )
}
