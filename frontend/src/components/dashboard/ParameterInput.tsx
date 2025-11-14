import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Activity } from "lucide-react";
import { parametersAPI } from "@/services/api";
import { useToast } from "@/hooks/use-toast";

interface Parameter {
  id: string;
  parameter_name: string;
  display_name: string;
  unit: string;
  normal_range_min: number;
  normal_range_max: number;
  category: string;
}

interface ParameterInputProps {
  initialValues?: Record<string, number>;
  onSubmit: (parameters: Record<string, number>) => void;
}

const ParameterInput = ({ initialValues = {}, onSubmit }: ParameterInputProps) => {
  const [parameters, setParameters] = useState<Parameter[]>([]);
  const [values, setValues] = useState<Record<string, number>>(initialValues);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    fetchParameters();
  }, []);

  const fetchParameters = async () => {
    try {
      const data = await parametersAPI.getParameters();
      setParameters(data || []);
    } catch (error: any) {
      console.error("Error fetching parameters:", error);
      toast({
        variant: "destructive",
        title: "Error loading parameters",
        description: error.message || "Could not load blood parameter definitions.",
      });
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(values);
  };

  const groupedParameters = parameters.reduce((acc, param) => {
    if (!acc[param.category]) {
      acc[param.category] = [];
    }
    acc[param.category].push(param);
    return acc;
  }, {} as Record<string, Parameter[]>);

  return (
    <Card className="shadow-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Activity className="h-5 w-5 text-secondary" />
          Manual Parameter Entry
        </CardTitle>
        <CardDescription>
          Enter your blood test values manually or update extracted values
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {Object.entries(groupedParameters).map(([category, params]) => (
            <div key={category} className="space-y-4">
              <h3 className="font-semibold text-lg text-foreground border-b pb-2">
                {category}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {params.map((param) => (
                  <div key={param.id} className="space-y-2">
                    <Label htmlFor={param.parameter_name} className="text-sm">
                      {param.display_name}
                      <span className="text-xs text-muted-foreground ml-2">
                        ({param.normal_range_min}-{param.normal_range_max} {param.unit})
                      </span>
                    </Label>
                    <Input
                      id={param.parameter_name}
                      type="number"
                      step="0.1"
                      placeholder={`Enter ${param.display_name.toLowerCase()}`}
                      value={values[param.parameter_name] || ""}
                      onChange={(e) =>
                        setValues({
                          ...values,
                          [param.parameter_name]: parseFloat(e.target.value) || 0,
                        })
                      }
                    />
                  </div>
                ))}
              </div>
            </div>
          ))}
          
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Analyzing..." : "Analyze Blood Parameters"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default ParameterInput;
