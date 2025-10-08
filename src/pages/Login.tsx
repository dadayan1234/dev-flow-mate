import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Code2, ArrowRight } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/hooks/useAuth";

const Login = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { signIn, user } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      navigate("/dashboard");
    }
  }, [user, navigate]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const { error } = await signIn(email, password);

      if (error) {
        toast({
          title: "Login failed",
          description: error.message || "Invalid credentials. Please try again.",
          variant: "destructive",
        });
      } else {
        toast({
          title: "Welcome back!",
          description: "Successfully logged in to DevNoteX",
        });
        navigate("/dashboard");
      }
    } catch (error: any) {
      toast({
        title: "Login failed",
        description: "An unexpected error occurred. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-background to-secondary/10 animate-pulse" />
      
      <Card className="w-full max-w-md glass-card relative z-10 p-8 space-y-6 animate-slide-up">
        {/* Logo */}
        <div className="flex items-center justify-center gap-2 mb-2">
          <div className="p-2 rounded-lg bg-primary/20 glow-purple">
            <Code2 className="h-8 w-8 text-primary" />
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            DevNoteX
          </h1>
        </div>
        
        <div className="text-center space-y-2">
          <h2 className="text-2xl font-semibold">Welcome Back</h2>
          <p className="text-muted-foreground">Sign in to your developer workspace</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="dev@devnotex.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="bg-muted/50 border-border/50 focus:border-primary transition-smooth"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="bg-muted/50 border-border/50 focus:border-primary transition-smooth"
            />
          </div>

          <Button
            type="submit"
            className="w-full bg-primary hover:bg-primary/90 transition-smooth group"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign In"}
            <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
          </Button>
        </form>

        <div className="text-center text-sm">
          <span className="text-muted-foreground">Don't have an account? </span>
          <Link to="/register" className="text-primary hover:underline font-medium">
            Create one
          </Link>
        </div>
      </Card>
    </div>
  );
};

export default Login;
