import { ReactNode } from "react";
import heroImage from "@/assets/hero-medical.jpg";

interface AuthLayoutProps {
  children: ReactNode;
  title: string;
  description: string;
}

const AuthLayout = ({ children, title, description }: AuthLayoutProps) => {
  return (
    <div className="min-h-screen grid lg:grid-cols-2">
      {/* Left side - Auth form */}
      <div className="flex items-center justify-center p-8 bg-gradient-subtle">
        <div className="w-full max-w-md space-y-8">
          <div className="text-center">
            <h1 className="text-2xl md:text-3xl font-bold bg-gradient-primary bg-clip-text text-transparent mb-2">
              Blood Parameter Analysis
            </h1>
            <h2 className="text-xl md:text-2xl font-semibold text-foreground mb-2">{title}</h2>
            <p className="text-muted-foreground">{description}</p>
          </div>
          {children}
        </div>
      </div>

      {/* Right side - Hero image */}
      <div className="hidden lg:block relative overflow-hidden">
        <img
          src={heroImage}
          alt="Medical data visualization representing advanced healthcare analytics"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-secondary/20" />
        <div className="absolute inset-0 flex items-center justify-center p-12">
          <div className="text-white text-center space-y-6">
            <h3 className="text-4xl font-bold drop-shadow-lg">
              Predictive Healthcare at Your Fingertips
            </h3>
            <p className="text-xl drop-shadow-md max-w-lg mx-auto">
              Advanced blood parameter analysis powered by AI to help you understand your health better
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
