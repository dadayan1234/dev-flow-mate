import { useEffect, useState, createContext, useContext, ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import api from "@/utils/api";

interface User {
  id: string;
  email: string;
  full_name: string;
  avatar_url: string | null;
  created_at: string;
  updated_at: string;
}

type AuthContextType = {
  user: User | null;
  loading: boolean;
  signUp: (email: string, password: string, fullName: string) => Promise<any>;
  signIn: (email: string, password: string) => Promise<any>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const storedUser = localStorage.getItem('user');

    if (token && storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
      }
    }

    setLoading(false);
  }, []);

  const signUp = async (email: string, password: string, fullName: string) => {
    try {
      const response = await api.post('/api/auth/register', {
        email,
        password,
        full_name: fullName,
      });

      const { access_token, user: userData } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));

      setUser(userData);

      return { data: response.data, error: null };
    } catch (error: any) {
      return {
        data: null,
        error: {
          message: error.response?.data?.detail || 'Registration failed',
        },
      };
    }
  };

  const signIn = async (email: string, password: string) => {
    try {
      const response = await api.post('/api/auth/login', {
        email,
        password,
      });

      const { access_token, user: userData } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));

      setUser(userData);

      return { data: response.data, error: null };
    } catch (error: any) {
      return {
        data: null,
        error: {
          message: error.response?.data?.detail || 'Login failed',
        },
      };
    }
  };

  const signOut = async () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
    navigate("/login");
  };

  const value: AuthContextType = {
    user,
    loading,
    signUp,
    signIn,
    signOut,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
};
