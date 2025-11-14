import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Heart, Activity, Droplet, Brain, AlertCircle } from "lucide-react";

interface DiseaseRisk {
  disease: string;
  risk_level: string;
  severity: number;
  indicators: string[];
  explanation: string;
  prevention?: string;
  symptoms?: string[];
}

interface DiseaseRisksProps {
  risks: DiseaseRisk[];
}

const DiseaseRisks = ({ risks }: DiseaseRisksProps) => {
  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case "low":
        return "border-success text-success";
      case "moderate":
        return "border-warning text-warning";
      case "high":
        return "border-destructive text-destructive";
      default:
        return "border-muted text-muted-foreground";
    }
  };

  const getIcon = (disease: string) => {
    const diseaseLower = disease.toLowerCase();
    if (diseaseLower.includes("heart") || diseaseLower.includes("cardio")) {
      return Heart;
    } else if (diseaseLower.includes("diabetes") || diseaseLower.includes("glucose")) {
      return Droplet;
    } else if (diseaseLower.includes("brain") || diseaseLower.includes("neuro")) {
      return Brain;
    } else if (diseaseLower.includes("pressure") || diseaseLower.includes("hypertension")) {
      return Activity;
    }
    return AlertCircle;
  };

  return (
    <Card className="shadow-card">
      <CardHeader>
        <CardTitle>Disease Risk Assessment</CardTitle>
        <CardDescription>Potential health risks based on your blood parameters</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {risks.map((risk, index) => {
          const Icon = getIcon(risk.disease);
          
          return (
            <div
              key={index}
              className="p-4 border-2 border-muted rounded-lg hover:border-primary/30 transition-colors space-y-3"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3 flex-1">
                  <div className="p-2 bg-primary/10 rounded-lg">
                    <Icon className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-base">{risk.disease}</h3>
                  </div>
                </div>
                <Badge variant="outline" className={getRiskColor(risk.risk_level)}>
                  {risk.risk_level}
                </Badge>
              </div>

              <div className="space-y-3">
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <span className="font-medium">Key Indicators:</span>
                  <div className="flex flex-wrap gap-1">
                    {risk.indicators.map((indicator, i) => (
                      <Badge key={i} variant="secondary" className="text-xs">
                        {indicator}
                      </Badge>
                    ))}
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <span className="text-xs font-medium">Severity:</span>
                  <div className="flex-1 bg-muted rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-full ${
                        risk.severity > 70 ? "bg-destructive" : risk.severity > 40 ? "bg-warning" : "bg-success"
                      }`}
                      style={{ width: `${risk.severity}%` }}
                    />
                  </div>
                  <span className="text-xs font-bold">{risk.severity}%</span>
                </div>
                
                <div className="pt-2 border-t space-y-2">
                  <div>
                    <p className="text-xs font-semibold text-foreground mb-1">Why This Occurs:</p>
                    <p className="text-xs text-muted-foreground leading-relaxed">{risk.explanation}</p>
                  </div>
                  
                  {risk.prevention && (
                    <div>
                      <p className="text-xs font-semibold text-foreground mb-1">Management & Prevention:</p>
                      <p className="text-xs text-muted-foreground leading-relaxed">{risk.prevention}</p>
                    </div>
                  )}
                  
                  {risk.symptoms && risk.symptoms.length > 0 && (
                    <div>
                      <p className="text-xs font-semibold text-foreground mb-1">Symptoms to Watch:</p>
                      <ul className="text-xs text-muted-foreground list-disc list-inside space-y-0.5">
                        {risk.symptoms.map((symptom, i) => (
                          <li key={i}>{symptom}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
};

export default DiseaseRisks;
