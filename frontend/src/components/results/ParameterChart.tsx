import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

interface ParameterChartProps {
  parameterAnalysis: Array<{
    parameter: string;
    value: number;
    normal_min?: number;
    normal_max?: number;
    status: string;
    concern_level: number;
    explanation?: string;
  }>;
}

const ParameterChart = ({ parameterAnalysis }: ParameterChartProps) => {
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "normal":
        return "#10b981"; // success color
      case "borderline":
        return "#f59e0b"; // warning color
      case "abnormal":
        return "#ef4444"; // destructive color
      case "critical":
        return "#dc2626"; // darker red
      default:
        return "#6b7280"; // muted color
    }
  };

  const chartData = parameterAnalysis.map((param) => ({
    name: param.parameter,
    value: param.value,
    normalMin: param.normal_min || 0,
    normalMax: param.normal_max || param.value * 1.2,
    fill: getStatusColor(param.status),
    status: param.status,
  }));

  return (
    <Card className="shadow-card">
      <CardHeader>
        <CardTitle>Blood Parameter Analysis</CardTitle>
        <CardDescription>Comparison of your values with normal ranges</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis 
                dataKey="name" 
                angle={-45} 
                textAnchor="end" 
                height={100}
                className="text-xs"
              />
              <YAxis className="text-xs" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '6px'
                }}
              />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              <Bar dataKey="value" name="Your Value" radius={[8, 8, 0, 0]} />
              <Bar dataKey="normalMax" name="Normal Max" fill="#94a3b8" opacity={0.3} />
            </BarChart>
          </ResponsiveContainer>

          {/* Detailed parameter explanations */}
          <div className="space-y-3 pt-4 border-t">
            <h3 className="font-semibold text-sm">Parameter Details:</h3>
            {parameterAnalysis.map((param, index) => (
              <div key={index} className="p-3 bg-muted/50 rounded-lg space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-sm">{param.parameter}</span>
                  <span className="text-xs" style={{ color: getStatusColor(param.status) }}>
                    {param.status}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <span>Value: <strong>{param.value}</strong></span>
                  {param.normal_min && param.normal_max && (
                    <span>| Normal: {param.normal_min} - {param.normal_max}</span>
                  )}
                </div>
                {param.explanation && (
                  <p className="text-xs text-muted-foreground pt-1 leading-relaxed">
                    {param.explanation}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ParameterChart;
