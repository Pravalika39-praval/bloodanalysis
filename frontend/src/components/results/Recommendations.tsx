import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Utensils, Dumbbell, HeartPulse, Stethoscope } from "lucide-react";

interface Recommendation {
  category: "lifestyle" | "diet" | "exercise" | "medical";
  priority: "high" | "medium" | "low";
  action: string;
  reasoning?: string;
  foods?: string[];
  exercises?: string[];
  duration?: string;
}

interface RecommendationsProps {
  recommendations: Recommendation[];
}

const Recommendations = ({ recommendations }: RecommendationsProps) => {
  const getCategoryConfig = (category: string) => {
    switch (category) {
      case "diet":
        return {
          icon: Utensils,
          color: "text-success",
          bgColor: "bg-success/10",
          label: "Diet",
        };
      case "exercise":
        return {
          icon: Dumbbell,
          color: "text-primary",
          bgColor: "bg-primary/10",
          label: "Exercise",
        };
      case "lifestyle":
        return {
          icon: HeartPulse,
          color: "text-warning",
          bgColor: "bg-warning/10",
          label: "Lifestyle",
        };
      case "medical":
        return {
          icon: Stethoscope,
          color: "text-destructive",
          bgColor: "bg-destructive/10",
          label: "Medical",
        };
      default:
        return {
          icon: HeartPulse,
          color: "text-muted-foreground",
          bgColor: "bg-muted",
          label: category,
        };
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "border-destructive text-destructive";
      case "medium":
        return "border-warning text-warning";
      case "low":
        return "border-success text-success";
      default:
        return "";
    }
  };

  // Group recommendations by category
  const groupedRecommendations = recommendations.reduce((acc, rec) => {
    if (!acc[rec.category]) {
      acc[rec.category] = [];
    }
    acc[rec.category].push(rec);
    return acc;
  }, {} as Record<string, Recommendation[]>);

  return (
    <Card className="shadow-card">
      <CardHeader>
        <CardTitle>Personalized Recommendations</CardTitle>
        <CardDescription>Tailored health improvement suggestions</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {Object.entries(groupedRecommendations).map(([category, recs]) => {
          const config = getCategoryConfig(category);
          const Icon = config.icon;

          return (
            <div key={category} className="space-y-3">
              <div className="flex items-center gap-2">
                <div className={`p-2 rounded-lg ${config.bgColor}`}>
                  <Icon className={`h-4 w-4 ${config.color}`} />
                </div>
                <h3 className="font-semibold text-base">{config.label}</h3>
              </div>

              <div className="space-y-3 ml-1">
                {recs.map((rec, index) => (
                  <div key={index} className="p-4 bg-muted/50 rounded-lg space-y-2 border-l-2 border-primary/30">
                    <div className="flex items-start justify-between mb-2">
                      <p className="text-sm font-semibold flex-1">{rec.action}</p>
                      <Badge variant="outline" className={getPriorityColor(rec.priority)}>
                        {rec.priority}
                      </Badge>
                    </div>
                    
                    {rec.reasoning && (
                      <p className="text-xs text-muted-foreground leading-relaxed">
                        <span className="font-medium text-foreground">Why: </span>{rec.reasoning}
                      </p>
                    )}
                    
                    {rec.foods && rec.foods.length > 0 && (
                      <div className="text-xs">
                        <span className="font-medium text-foreground">Foods: </span>
                        <span className="text-muted-foreground">{rec.foods.join(", ")}</span>
                      </div>
                    )}
                    
                    {rec.exercises && rec.exercises.length > 0 && (
                      <div className="text-xs">
                        <span className="font-medium text-foreground">Exercises: </span>
                        <span className="text-muted-foreground">{rec.exercises.join(", ")}</span>
                      </div>
                    )}
                    
                    {rec.duration && (
                      <div className="text-xs">
                        <span className="font-medium text-foreground">Duration: </span>
                        <span className="text-muted-foreground">{rec.duration}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
};

export default Recommendations;
