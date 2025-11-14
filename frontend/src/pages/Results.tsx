import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Upload, History, Volume2, VolumeX } from "lucide-react";
import RiskAssessment from "@/components/results/RiskAssessment";
import ParameterChart from "@/components/results/ParameterChart";
import DiseaseRisks from "@/components/results/DiseaseRisks";
import Recommendations from "@/components/results/Recommendations";
import { useState, useEffect } from "react";
import { tts } from "@/utils/textToSpeech";
import LanguageSelector from "@/components/LanguageSelector";
import bgMedical from "@/assets/bg-medical-analysis.jpg";

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { analysis, parameters } = location.state || {};
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [language, setLanguage] = useState("en");

  useEffect(() => {
    // Get language from localStorage or default to 'en'
    const storedLanguage = localStorage.getItem("selectedLanguage") || "en";
    setLanguage(storedLanguage);
  }, []);

  const generateSpeechText = () => {
    let text = `Health Analysis Results. `;
    text += `Overall risk score: ${analysis.overall_risk_score} out of 100. `;
    text += `Risk level: ${analysis.risk_level}. `;
    text += `Summary: ${analysis.summary}. `;
    
    if (analysis.disease_risks && analysis.disease_risks.length > 0) {
      text += `Predicted diseases: `;
      analysis.disease_risks.forEach((risk: any) => {
        text += `${risk.disease} with ${risk.risk_level} risk. `;
        if (risk.explanation) {
          text += `${risk.explanation}. `;
        }
        if (risk.prevention) {
          text += `Prevention: ${risk.prevention}. `;
        }
      });
    }

    if (analysis.recommendations && analysis.recommendations.length > 0) {
      text += `Recommendations: `;
      analysis.recommendations.forEach((rec: any) => {
        text += `${rec.action}. `;
        if (rec.reasoning) {
          text += `${rec.reasoning}. `;
        }
      });
    }

    return text;
  };

  const toggleSpeech = () => {
    if (isSpeaking) {
      tts.stop();
      setIsSpeaking(false);
    } else {
      const speechText = generateSpeechText();
      tts.speak(speechText, language);
      setIsSpeaking(true);
      
      // Listen for speech end
      setTimeout(() => {
        setIsSpeaking(false);
      }, 100);
    }
  };

  useEffect(() => {
    return () => {
      tts.stop();
    };
  }, []);

  if (!analysis) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-subtle">
        <div className="text-center space-y-4">
          <h2 className="text-2xl font-bold">No Analysis Data</h2>
          <p className="text-muted-foreground">Please upload a report or enter parameters first.</p>
          <Button onClick={() => navigate("/")}>Go to Dashboard</Button>
        </div>
      </div>
    );
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
            <div className="flex items-center gap-2">
              <LanguageSelector
                value={language}
                onChange={(v) => {
                  setLanguage(v);
                  localStorage.setItem("selectedLanguage", v);
                }}
              />
              <Button 
                variant={isSpeaking ? "default" : "ghost"} 
                size="sm" 
                onClick={toggleSpeech}
              >
                {isSpeaking ? (
                  <>
                    <VolumeX className="h-4 w-4 mr-2" />
                    Stop Audio
                  </>
                ) : (
                  <>
                    <Volume2 className="h-4 w-4 mr-2" />
                    Listen to Results
                  </>
                )}
              </Button>
              <Button variant="ghost" size="sm" onClick={() => navigate("/")}>
                <Upload className="h-4 w-4 mr-2" />
                New Analysis
              </Button>
              <Button variant="ghost" size="sm" onClick={() => navigate("/history")}>
                <History className="h-4 w-4 mr-2" />
                History
              </Button>
            </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 space-y-8 relative z-10">
        <div className="flex items-center gap-4 mb-6">
          <Button variant="ghost" size="sm" onClick={() => navigate("/")}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
        </div>

        <div className="text-center space-y-2 mb-8">
          <h2 className="text-3xl font-bold text-foreground">Health Analysis Results</h2>
          <p className="text-muted-foreground">
            Comprehensive AI-powered insights from your blood parameters
          </p>
        </div>

        {/* Risk Assessment */}
        <RiskAssessment
          riskScore={analysis.overall_risk_score}
          riskLevel={analysis.risk_level}
          summary={analysis.summary}
        />

        {/* Parameter Chart */}
        {analysis.parameter_analysis && analysis.parameter_analysis.length > 0 && (
          <ParameterChart parameterAnalysis={analysis.parameter_analysis} />
        )}

        {/* Disease Risks and Recommendations */}
        <div className="grid lg:grid-cols-2 gap-8">
          {analysis.disease_risks && analysis.disease_risks.length > 0 && (
            <DiseaseRisks risks={analysis.disease_risks} />
          )}
          {analysis.recommendations && analysis.recommendations.length > 0 && (
            <Recommendations recommendations={analysis.recommendations} />
          )}
        </div>
      </main>
    </div>
  );
};

export default Results;
