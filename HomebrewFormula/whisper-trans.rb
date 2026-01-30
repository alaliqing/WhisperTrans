cask "whisper-trans" do
  version "1.0.0"

  # Apple Silicon (ARM64) only
  url "https://github.com/alaliqing/WhisperTrans/releases/download/v#{version}/WhisperTrans-#{version}-arm64.dmg"
  sha256 "0ddb28013a32dfd4c9e038a2670d7bebf350d4b943638d1d06c953557f498f63"

  name "WhisperTrans"
  desc "Simple audio transcription tool using OpenAI's Whisper AI model"
  homepage "https://github.com/alaliqing/WhisperTrans"

  app "WhisperTrans.app"

  # Cleanup caches and configuration
  zap trash: [
    "~/.whispertrans",
    "~/Library/Application Support/WhisperTrans",
    "~/Library/Caches/WhisperTrans",
  ]

  # Caveats for first-time users
  caveats do
    <<~EOS
      WhisperTrans uses OpenAI's Whisper AI model for transcription.

      On first launch, the app will download the selected AI model (75MB - 3GB).
      This is a one-time download and the models will be cached for future use.

      For Intel Mac users: Install from source via git clone (see README).

      For more information, visit: https://github.com/alaliqing/WhisperTrans
    EOS
  end
end
