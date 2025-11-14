import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import UploadSection from "@/components/dashboard/UploadSection";
import LanguageSelector from "@/components/LanguageSelector";
import LoadingAnalysis from "@/components/LoadingAnalysis";
import { Activity, Shield, TrendingUp, LogOut, History, Info } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import bgMedical from "@/assets/bg-medical-analysis.jpg";
import { authAPI, reportsAPI } from "@/services/api";

const Dashboard = () => {
  const [parameters, setParameters] = useState<Record<string, number>>({});
  const [language, setLanguage] = useState("en");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [user, setUser] = useState<any>(null);
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    checkUser();
    // Initialize language from localStorage if available
    const stored = localStorage.getItem("selectedLanguage");
    if (stored) setLanguage(stored);
  }, []);

  // Persist language selection so it stays unchanged across pages/reloads
  useEffect(() => {
    localStorage.setItem("selectedLanguage", language);
  }, [language]);

  const checkUser = async () => {
    if (!authAPI.isAuthenticated()) {
      navigate("/login");
      return;
    }

    try {
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error("Auth error:", error);
      navigate("/login");
    }
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      toast({
        title: "Logged out",
        description: "You have been successfully logged out.",
      });
      navigate("/login");
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Logout failed",
        description: error.message,
      });
    }
  };

  const handleAnalyze = async (params: Record<string, number>) => {
    setIsAnalyzing(true);
    // Store language preference
    localStorage.setItem("selectedLanguage", language);
    
    try {
      const result = await reportsAPI.analyzeReport(params);

      // Navigate to results with the analysis data
      navigate("/results", { 
        state: { 
          analysis: result.analysis, 
          parameters: params 
        } 
      });
    } catch (error: any) {
      setIsAnalyzing(false);
      toast({
        variant: "destructive",
        title: "Analysis failed",
        description: error.message || "Could not analyze blood parameters",
      });
    }
  };

  if (isAnalyzing) {
    return <LoadingAnalysis />;
  }

  return (
    <div className="min-h-screen bg-gradient-subtle relative">
      <div 
        className="absolute inset-0 opacity-60 bg-cover bg-center bg-fixed"
        style={{ backgroundImage: `url(${bgMedical})` }}
      />
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-10 shadow-sm relative">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl md:text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            Blood Parameter Analysis for Predictive Health Care
          </h1>
          <div className="flex items-center gap-4">
            <LanguageSelector value={language} onChange={setLanguage} />
            <Button variant="ghost" size="sm" onClick={() => navigate("/history")}>
              <History className="h-4 w-4 mr-2" />
              History
            </Button>
            <Button variant="ghost" size="sm" onClick={() => navigate("/about")}>
              <Info className="h-4 w-4 mr-2" />
              About
            </Button>
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 space-y-8 max-w-6xl relative z-10">
        <div className="text-center space-y-3 mb-8">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground">AI-Powered Health Analysis</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto text-lg">
            Upload your blood report for comprehensive AI analysis and personalized health insights
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <Card className="shadow-card border-2 border-primary/20">
            <CardHeader>
              <Activity className="h-10 w-10 text-primary mb-2" />
              <CardTitle className="text-lg">Accurate Analysis</CardTitle>
              <CardDescription>AI-powered analysis of blood parameters with precision</CardDescription>
            </CardHeader>
          </Card>
          <Card className="shadow-card border-2 border-primary/20">
            <CardHeader>
              <Shield className="h-10 w-10 text-primary mb-2" />
              <CardTitle className="text-lg">Disease Prediction</CardTitle>
              <CardDescription>Early detection of potential health risks and diseases</CardDescription>
            </CardHeader>
          </Card>
          <Card className="shadow-card border-2 border-primary/20">
            <CardHeader>
              <TrendingUp className="h-10 w-10 text-primary mb-2" />
              <CardTitle className="text-lg">Personalized Plans</CardTitle>
              <CardDescription>Custom diet and exercise recommendations</CardDescription>
            </CardHeader>
          </Card>
        </div>

        <div className="max-w-2xl mx-auto">
          <UploadSection onAnalysisComplete={handleAnalyze} />
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
