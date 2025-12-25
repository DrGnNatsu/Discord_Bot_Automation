import "@/app/LandingPage.css"
import {Button} from "@/components/ui/button.tsx";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card.tsx";
import {MessageSquare, Settings, Zap} from "lucide-react";

const features = [
    {
        title: "Custom Configuration",
        description: "Intuitive interface to customize bot behavior, commands, and features without code",
        icon: Settings
    },
    {
        title: "Custom Commands",
        description: "Create and manage custom commands with flexible triggers and actions",
        icon: MessageSquare
    },
    {
        title: "Lightning Fast",
        description: "Optimized performance ensures your bot responds instantly to every command",
        icon: Zap
    }
]

export default function LandingPage() {
  return (
    <div className="landing-root">
      {/* Hero Section */}
      <section className="landing-hero">
        <div className="hero-content-wrapper">
          <h1 className="hero-title">
            Manage Your Discord Bot <span className="text-primary">Like a Pro</span>
          </h1>
          <p className="hero-subtitle">
            A powerful admin dashboard to control, monitor, and optimize your Discord bot with ease. Real-time
            analytics, user management, and advanced configuration—all in one place.
          </p>
          <div className="hero-actions">
            <Button size="lg" className="text-base">
              Get Started
            </Button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="features-section">
        <div className="features-wrapper">
          <h2 className="features-title">
            Everything You Need to <span className="text-primary">Succeed</span>
          </h2>

          <div className="features-grid">
            {features.map((feature) => 
            <Card>
              <CardHeader>
                <feature.icon className="feature-icon" />
                <CardTitle>{feature.title}</CardTitle>
                <CardDescription>{feature.description}</CardDescription>
              </CardHeader>
            </Card>
            )}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-wrapper">
          <Card className="cta-card">
            <CardContent className="cta-content">
              <h2 className="cta-title">Ready to Take Control?</h2>
              <p className="cta-description">
                Join thousands of Discord communities using our admin dashboard to manage their bots efficiently.
              </p>
              <Button size="lg" className="cta-button">
                Start Managing Your Bot
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  )
}