import AuthLayout from "@/components/auth/AuthLayout";
import LoginForm from "@/components/auth/LoginForm";

const Login = () => {
  return (
    <AuthLayout
      title="Welcome Back"
      description="Log in to access your health analytics dashboard"
    >
      <LoginForm />
    </AuthLayout>
  );
};

export default Login;
