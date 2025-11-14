import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import { ArrowLeft, Calendar, TrendingUp, Eye } from "lucide-react";
import bgMedical from "@/assets/bg-medical-analysis.jpg";
import { authAPI, reportsAPI } from "@/services/api";

interface BloodReport {
  id: string;
  created_at: string;
  overall_risk: string;
  risk_score: number;
  parameters: any;
  analysis: any;
}

const History = () => {
  const [reports, setReports] = useState<BloodReport[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    if (!authAPI.isAuthenticated()) {
      navigate("/login");
      return;
    }

    try {
      const data = await reportsAPI.getHistory();
      setReports(data);
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error loading history",
        description: error.message || "Could not fetch your blood report history.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getRiskBadge = (score: number) => {
    if (score < 30) return <Badge className="bg-success/10 text-success border-success">Low Risk</Badge>;
    if (score < 60) return <Badge className="bg-warning/10 text-warning border-warning">Moderate Risk</Badge>;
    if (score < 80) return <Badge className="bg-destructive/10 text-destructive border-destructive">High Risk</Badge>;
    return <Badge className="bg-destructive/20 text-destructive border-destructive">Critical</Badge>;
  };

  const viewReport = async (reportId: string) => {
    try {
      const report = await reportsAPI.getReport(reportId);
      navigate("/results", {
        state: {
          analysis: report.analysis,
          parameters: report.parameters,
        },
      });
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Failed to load report",
        description: error.message || "Could not load the selected report.",
      });
    }
  };

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

        <div className="text-center space-y-2 mb-8">
          <h2 className="text-3xl font-bold text-foreground">Analysis History</h2>
          <p className="text-muted-foreground">View your past blood parameter analyses</p>
        </div>

        {isLoading ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Loading your history...</p>
          </div>
        ) : reports.length === 0 ? (
          <Card className="shadow-card">
            <CardContent className="py-12 text-center">
              <TrendingUp className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <h3 className="text-lg font-semibold mb-2">No Reports Yet</h3>
              <p className="text-muted-foreground mb-4">
                Start by uploading your first blood report or entering parameters manually
              </p>
              <Button onClick={() => navigate("/")}>Create First Analysis</Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {reports.map((report) => (
              <Card
                key={report.id}
                className="shadow-card hover:shadow-elegant transition-all duration-300 cursor-pointer"
                onClick={() => viewReport(report.id)}
              >
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="flex items-center gap-2">
                      <Calendar className="h-4 w-4" />
                      {new Date(report.created_at).toLocaleDateString()}
                    </span>
                    {getRiskBadge(report.risk_score)}
                  </CardTitle>
                  <CardDescription>
                    Analyzed on {new Date(report.created_at).toLocaleDateString()}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Risk Score</span>
                    <span className="text-xl font-bold text-primary">{report.risk_score}/100</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div
                      className="h-full bg-gradient-primary rounded-full transition-all duration-500"
                      style={{ width: `${report.risk_score}%` }}
                    />
                  </div>
                  <Button variant="outline" className="w-full" size="sm">
                    <Eye className="h-4 w-4 mr-2" />
                    View Full Analysis
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default History;
