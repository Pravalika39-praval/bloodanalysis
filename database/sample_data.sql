-- Insert blood parameters with normal ranges
INSERT INTO blood_parameters (parameter_name, normal_min, normal_max, unit, category) VALUES
('WBC', 4.5, 10.0, '×10⁹/L', 'White Blood Cells'),
('RBC', 4.2, 5.4, '×10⁶/µL', 'Red Blood Cells'),
('HGB', 12.0, 16.0, 'g/dL', 'Hemoglobin'),
('HCT', 36.1, 44.3, '%', 'Hematocrit'),
('MCV', 80, 100, 'fL', 'Red Cell Indices'),
('MCH', 27, 31, 'pg', 'Red Cell Indices'),
('MCHC', 33, 36, 'g/dL', 'Red Cell Indices'),
('PLT', 150, 400, '×10³/µL', 'Platelets'),
('RDW-SD', 39, 46, 'fL', 'Red Cell Distribution'),
('RDW-CV', 11.6, 14.6, '%', 'Red Cell Distribution'),
('PDW', 10, 17, 'fL', 'Platelet Indices'),
('MPV', 7.5, 11.5, 'fL', 'Platelet Indices'),
('P-LCR', 13, 43, '%', 'Platelet Indices'),
('PCT', 0.1, 0.5, '%', 'Platelet Indices'),
('NEUT', 1.5, 8.0, '×10⁹/L', 'Differential Count'),
('LYMPH', 1.0, 4.0, '×10⁹/L', 'Differential Count'),
('MONO', 0.2, 0.8, '×10⁹/L', 'Differential Count'),
('EO', 0.04, 0.4, '×10⁹/L', 'Differential Count'),
('BASO', 0.0, 0.2, '×10⁹/L', 'Differential Count'),
('IG', 0.0, 0.05, '×10⁹/L', 'Immature Granulocytes'),
('NRBC', 0, 0, '/100 WBC', 'Nucleated RBC'),
('RETICULOCYTES', 0.5, 2.5, '%', 'Reticulocytes'),
('IRF', 0.48, 27.0, '%', 'Reticulocyte Fractions'),
('LFR', 87.0, 91.4, '%', 'Reticulocyte Fractions'),
('MFR', 11.0, 18.0, '%', 'Reticulocyte Fractions'),
('HFR', 0.0, 1.7, '%', 'Reticulocyte Fractions');

-- Insert common diseases
INSERT INTO diseases (disease_name, description, symptoms, prevention) VALUES
('Iron Deficiency Anemia', 'A condition where lack of iron leads to reduced hemoglobin production', 'Fatigue, weakness, pale skin, shortness of breath', 'Iron-rich diet, vitamin C for absorption'),
('Vitamin B12 Deficiency', 'Insufficient B12 affecting red blood cell production', 'Fatigue, neurological symptoms, sore tongue', 'B12-rich foods or supplements'),
('Thrombocytopenia', 'Low platelet count affecting blood clotting', 'Easy bruising, prolonged bleeding, petechiae', 'Avoid blood thinners, protect from injury'),
('Leukocytosis', 'High white blood cell count indicating infection or inflammation', 'Fever, fatigue, body aches', 'Treat underlying infection, maintain hygiene'),
('Leukopenia', 'Low white blood cell count increasing infection risk', 'Frequent infections, fever, fatigue', 'Good hygiene, avoid sick people'),
('Polycythemia', 'Excess red blood cells thickening blood', 'Headache, dizziness, itching', 'Stay hydrated, regular blood tests'),
('Microcytic Anemia', 'Small red blood cells due to iron deficiency', 'Fatigue, weakness, pale skin', 'Iron supplementation, balanced diet'),
('Macrocytic Anemia', 'Large red blood cells due to B12/folate deficiency', 'Fatigue, neurological issues, digestive problems', 'B12/folate supplements');

-- Insert recommendations
INSERT INTO recommendations (disease_id, category, recommendation_text, duration_weeks, priority_level) VALUES
(1, 'Diet', 'Increase iron-rich foods: red meat, spinach, lentils, fortified cereals. Combine with vitamin C sources for better absorption.', 12, 'High'),
(1, 'Exercise', 'Start with light walking 20-30 minutes daily. Gradually increase intensity as energy levels improve.', 8, 'Medium'),
(1, 'Lifestyle', 'Avoid tea/coffee with meals as they inhibit iron absorption. Get adequate sleep (7-8 hours).', 4, 'High'),
(2, 'Diet', 'Consume B12-rich foods: meat, fish, eggs, dairy. Consider B12 supplements if vegetarian.', 12, 'High'),
(2, 'Exercise', 'Moderate exercise 30 minutes daily. Include balance exercises for neurological symptoms.', 8, 'Medium'),
(3, 'Lifestyle', 'Avoid contact sports and activities with injury risk. Use soft toothbrush, electric razor.', 52, 'High'),
(4, 'Medical', 'Complete prescribed antibiotic course. Rest and hydrate adequately.', 2, 'High'),
(5, 'Lifestyle', 'Practice good hand hygiene. Avoid crowded places during flu season.', 52, 'High');