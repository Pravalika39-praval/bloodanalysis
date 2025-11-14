import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, Brain, Shield, Zap, Globe, BarChart, Heart } from "lucide-react";
import heroImage from "@/assets/hero-medical.jpg";
import bgMedical from "@/assets/bg-medical-analysis.jpg";

const About = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning algorithms analyze your blood parameters for accurate health insights",
    },
    {
      icon: Shield,
      title: "Secure & Private",
      description: "Your health data is encrypted and stored securely with enterprise-grade security",
    },
    {
      icon: Zap,
      title: "Instant Results",
      description: "Get comprehensive health analysis in seconds, not days",
    },
    {
      icon: Globe,
      title: "Multilingual Support",
      description: "Access health insights in your preferred language for better understanding",
    },
    {
      icon: BarChart,
      title: "Visual Analytics",
      description: "Interactive charts and graphs make complex data easy to understand",
    },
    {
      icon: Heart,
      title: "Personalized Recommendations",
      description: "Receive tailored health advice based on your unique blood parameters",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-subtle relative">
      <div 
        className="absolute inset-0 opacity-60 bg-cover bg-center bg-fixed"
        style={{ backgroundImage: `url(${bgMedical})` }}
      />
      <header className="border-b bg-card/50 backdrop-blur-sm relative z-10">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-xl md:text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            Blood Parameter Analysis for Predictive Health Care
          </h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 relative z-10">
        <div className="flex items-center gap-4 mb-6">
          <Button variant="ghost" size="sm" onClick={() => navigate("/")}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
        </div>

        {/* Hero Section */}
        <div className="relative rounded-2xl overflow-hidden mb-12 shadow-elegant">
          <img
            src={heroImage}
            alt="Blood Parameter Analysis - Predictive Healthcare"
            className="w-full h-[300px] object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-primary/80 to-secondary/80 flex items-center justify-center">
            <div className="text-center text-white px-4">
              <h2 className="text-4xl font-bold mb-4">About Blood Parameter Analysis</h2>
              <p className="text-xl max-w-2xl">
                Revolutionizing healthcare through AI-powered blood parameter analysis
              </p>
            </div>
          </div>
        </div>

        {/* Mission Statement */}
        <Card className="shadow-card mb-12">
          <CardHeader>
            <CardTitle className="text-2xl">Our Mission</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-muted-foreground leading-relaxed">
            <p>
              Blood Parameter Analysis is dedicated to making predictive healthcare accessible to everyone. We believe
              that understanding your health should be simple, fast, and accurate.
            </p>
            <p>
              By leveraging cutting-edge artificial intelligence and medical expertise, we transform complex blood
              test results into actionable health insights. Our platform empowers individuals to take control of
              their health journey with data-driven recommendations.
            </p>
          </CardContent>
        </Card>

        {/* Features Grid */}
        <div className="mb-12">
          <h3 className="text-2xl font-bold text-center mb-8">Why Choose Blood Parameter Analysis?</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card key={index} className="shadow-card hover:shadow-elegant transition-shadow duration-300">
                  <CardHeader>
                    <div className="p-3 rounded-full bg-gradient-primary w-fit mb-2">
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <CardTitle>{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-sm leading-relaxed">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>

        {/* How It Works */}
        <Card className="shadow-card mb-12">
          <CardHeader>
            <CardTitle className="text-2xl">How It Works</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-start gap-4">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary text-white font-bold shrink-0">
                1
              </div>
              <div>
                <h4 className="font-semibold mb-2">Upload or Enter Data</h4>
                <p className="text-muted-foreground">
                  Upload your blood report or manually enter your blood parameter values
                </p>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary text-white font-bold shrink-0">
                2
              </div>
              <div>
                <h4 className="font-semibold mb-2">AI Analysis</h4>
                <p className="text-muted-foreground">
                  Our advanced AI analyzes your parameters against medical databases and research
                </p>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary text-white font-bold shrink-0">
                3
              </div>
              <div>
                <h4 className="font-semibold mb-2">Get Insights</h4>
                <p className="text-muted-foreground">
                  Receive comprehensive health insights, risk assessments, and personalized recommendations
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Disclaimer */}
        <Card className="shadow-card border-warning/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-warning" />
              Medical Disclaimer
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground space-y-2">
            <p>
              Blood Parameter Analysis is an AI-powered analysis tool designed to provide health insights based on
              blood parameters. It is not a substitute for professional medical advice, diagnosis, or treatment.
            </p>
            <p>
              Always consult with a qualified healthcare provider regarding any medical condition or health
              concerns. Never disregard professional medical advice or delay seeking it because of information
              provided by this platform.
            </p>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default About;
