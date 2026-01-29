cask "whisper-trans" do
  version "1.0.0"

  # Architecture-aware URLs and checksums
  if Hardware::CPU.arm?
    url "https://github.com/alaliqing/WhisperTrans/releases/download/v#{version}/WhisperTrans-#{version}-arm64.dmg"
    sha256 "ARM64_SHA256_PLACEHOLDER"  # Update after first build
  else
    url "https://github.com/alaliqing/WhisperTrans/releases/download/v#{version}/WhisperTrans-#{version}-x86_64.dmg"
    sha256 "X86_64_SHA256_PLACEHOLDER"  # Update after first build
  end

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

      For more information, visit: https://github.com/alaliqing/WhisperTrans
    EOS
  end
end
