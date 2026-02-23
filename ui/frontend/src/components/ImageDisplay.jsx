export default function ImageDisplay({ scoutData }) {
  const imageUrl = scoutData?.media?.images?.[0]?.src?.url
  if (!imageUrl) return null

  return (
    <div className="image-section">
      <h3 className="section-title">🖼️ Related Imagery</h3>
      <img className="context-image" src={imageUrl} alt="AI-selected contextual image" />
      <p className="image-caption">AI-selected contextual image</p>
    </div>
  )
}
