import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, CheckCircle, AlertCircle, XCircle } from "lucide-react";

interface RiskAssessmentProps {
  riskScore: number;
  riskLevel: "low" | "moderate" | "high" | "critical";
  summary: string;
}

const RiskAssessment = ({ riskScore, riskLevel, summary }: RiskAssessmentProps) => {
  const getRiskConfig = () => {
    switch (riskLevel) {
      case "low":
        return {
          icon: CheckCircle,
          color: "text-success",
          bgColor: "bg-success/10",
          borderColor: "border-success",
          label: "Low Risk",
        };
      case "moderate":
        return {
          icon: AlertCircle,
          color: "text-warning",
          bgColor: "bg-warning/10",
          borderColor: "border-warning",
          label: "Moderate Risk",
        };
      case "high":
        return {
          icon: AlertTriangle,
          color: "text-destructive",
          bgColor: "bg-destructive/10",
          borderColor: "border-destructive",
          label: "High Risk",
        };
      case "critical":
        return {
          icon: XCircle,
          color: "text-destructive",
          bgColor: "bg-destructive/20",
          borderColor: "border-destructive",
          label: "Critical Risk",
        };
    }
  };

  const config = getRiskConfig();
  const Icon = config.icon;

  return (
    <Card className={`shadow-card border-2 ${config.borderColor}`}>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Overall Risk Assessment</span>
          <Badge variant="outline" className={`${config.bgColor} ${config.color}`}>
            {config.label}
          </Badge>
        </CardTitle>
        <CardDescription>Based on comprehensive blood parameter analysis</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-4">
          <div className={`p-4 rounded-full ${config.bgColor}`}>
            <Icon className={`h-8 w-8 ${config.color}`} />
          </div>
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium">Risk Score</span>
              <span className={`text-2xl font-bold ${config.color}`}>{riskScore}/100</span>
            </div>
            <div className="w-full bg-muted rounded-full h-3 overflow-hidden">
              <div
                className={`h-full ${config.bgColor} ${config.color} transition-all duration-500`}
                style={{ width: `${riskScore}%` }}
              />
            </div>
          </div>
        </div>
        
        <div className="pt-4 border-t">
          <p className="text-sm text-foreground leading-relaxed">{summary}</p>
        </div>
      </CardContent>
    </Card>
  );
};

export default RiskAssessment;
