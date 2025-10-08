import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Code2, Plus, FolderKanban, CheckCircle2, Clock, Search, LogOut } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { supabase } from "@/integrations/supabase/client";
import { useToast } from "@/hooks/use-toast";

interface Project {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
}

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, signOut } = useAuth();
  const { toast } = useToast();
  const [searchQuery, setSearchQuery] = useState("");
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate("/login");
      return;
    }

    fetchProjects();
  }, [user, navigate]);

  const fetchProjects = async () => {
    try {
      const { data, error } = await supabase
        .from("projects")
        .select("*")
        .order("created_at", { ascending: false });

      if (error) throw error;
      setProjects(data || []);
    } catch (error: any) {
      console.error("Error fetching projects:", error);
      toast({
        title: "Error loading projects",
        description: error.message,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const filteredProjects = projects.filter((project) =>
    project.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleLogout = async () => {
    await signOut();
    navigate("/login");
  };

  return (
    <div className="min-h-screen p-6 space-y-6">
      {/* Header */}
      <header className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/20 glow-purple">
            <Code2 className="h-6 w-6 text-primary" />
          </div>
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              DevNoteX
            </h1>
            <p className="text-sm text-muted-foreground">Developer Workspace</p>
          </div>
        </div>
        
        <Button
          variant="outline"
          onClick={handleLogout}
          className="border-border/50 hover:border-destructive hover:text-destructive transition-smooth"
        >
          <LogOut className="mr-2 h-4 w-4" />
          Logout
        </Button>
      </header>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="glass-card p-6 space-y-2 hover:border-primary/50 transition-smooth">
          <div className="flex items-center gap-2 text-primary">
            <FolderKanban className="h-5 w-5" />
            <span className="text-sm font-medium">Active Projects</span>
          </div>
          <p className="text-3xl font-bold">{projects.length}</p>
        </Card>

        <Card className="glass-card p-6 space-y-2 hover:border-secondary/50 transition-smooth">
          <div className="flex items-center gap-2 text-secondary">
            <CheckCircle2 className="h-5 w-5" />
            <span className="text-sm font-medium">Total Projects</span>
          </div>
          <p className="text-3xl font-bold">{projects.length}</p>
        </Card>

        <Card className="glass-card p-6 space-y-2 hover:border-accent/50 transition-smooth">
          <div className="flex items-center gap-2 text-accent">
            <Clock className="h-5 w-5" />
            <span className="text-sm font-medium">Your Workspace</span>
          </div>
          <p className="text-sm font-medium text-muted-foreground">
            {user?.email}
          </p>
        </Card>
      </div>

      {/* Projects Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search projects..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 bg-muted/50 border-border/50 focus:border-primary transition-smooth"
            />
          </div>
          
          <Button className="bg-primary hover:bg-primary/90 transition-smooth group">
            <Plus className="mr-2 h-4 w-4" />
            New Project
          </Button>
        </div>

        {/* Projects Grid */}
        {loading ? (
          <Card className="glass-card p-12 text-center">
            <p className="text-muted-foreground">Loading projects...</p>
          </Card>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredProjects.map((project) => (
                <Card
                  key={project.id}
                  className="glass-card p-6 space-y-4 hover:border-primary/50 hover:shadow-lg cursor-pointer transition-smooth group"
                  onClick={() => navigate(`/project/${project.id}`)}
                >
                  <div className="space-y-2">
                    <h3 className="text-xl font-semibold group-hover:text-primary transition-colors">
                      {project.name}
                    </h3>
                    <p className="text-sm text-muted-foreground line-clamp-2">
                      {project.description || "No description"}
                    </p>
                  </div>

                  <div className="flex items-center justify-between text-xs text-muted-foreground pt-2 border-t border-border/50">
                    <span>Created</span>
                    <span>{new Date(project.created_at).toLocaleDateString()}</span>
                  </div>
                </Card>
              ))}
            </div>

            {filteredProjects.length === 0 && !loading && (
              <Card className="glass-card p-12 text-center space-y-4">
                <div>
                  <FolderKanban className="h-12 w-12 mx-auto mb-4 opacity-50 text-primary" />
                  <p className="text-muted-foreground text-lg font-medium">No projects yet</p>
                  <p className="text-sm text-muted-foreground mt-2">
                    Create your first project to get started
                  </p>
                </div>
                <Button className="bg-primary hover:bg-primary/90" onClick={() => toast({ title: "Coming soon!", description: "Project creation will be available soon" })}>
                  <Plus className="mr-2 h-4 w-4" />
                  Create Your First Project
                </Button>
              </Card>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
