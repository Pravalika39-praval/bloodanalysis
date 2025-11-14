import AuthLayout from "@/components/auth/AuthLayout";
import SignupForm from "@/components/auth/SignupForm";

const Signup = () => {
  return (
    <AuthLayout
      title="Create Your Account"
      description="Start your journey to better health insights"
    >
      <SignupForm />
    </AuthLayout>
  );
};

export default Signup;
