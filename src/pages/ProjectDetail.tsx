import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ArrowLeft, Github, Users, Settings, FileText, ListTodo, BookOpen } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import api from "@/utils/api";
import { useToast } from "@/hooks/use-toast";

const ProjectDetail = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState("notes");

  const { user } = useAuth();
  const { toast } = useToast();

  const project = {
    id: id || "",
    name: "DevNoteX Platform",
    description: "Main platform development with React and FastAPI backend",
    repoUrl: "https://github.com/devnotex/platform",
    members: 4,
  };

  const handleCreateItem = async (table: 'tasks' | 'notes' | 'documents', defaultTitle: string) => {
    if (!user || !id) {
      toast({ title: "Error", description: "User or Project ID missing.", variant: "destructive" });
      return;
    }

    try {
      const payload: any = {
        title: defaultTitle,
      };

      if (table === 'tasks') {
        payload.status = 'todo';
      }

      await api.post(`/api/projects/${id}/${table}`, payload);

      const itemName = table.charAt(0).toUpperCase() + table.slice(1);
      toast({
        title: `${itemName} created!`,
        description: `New ${itemName.toLowerCase()} added to ${project.name}.`,
      });

    } catch (error: any) {
      toast({
        title: `Error creating item`,
        description: error.response?.data?.detail || 'Failed to create item. Check project membership.',
        variant: "destructive",
      });
    }
  };

  const handleNewNote = () => handleCreateItem('notes', 'Untitled Note');
  const handleNewTask = () => handleCreateItem('tasks', 'New Task Title');
  const handleNewDocument = () => handleCreateItem('documents', 'New Document');

  return (
    <div className="min-h-screen p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="outline"
            size="icon"
            onClick={() => navigate("/dashboard")}
            className="border-border/50 hover:border-primary transition-smooth"
          >
            <ArrowLeft className="h-4 w-4" />
          </Button>

          <div>
            <h1 className="text-3xl font-bold">{project.name}</h1>
            <p className="text-muted-foreground">{project.description}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            className="border-border/50 hover:border-primary transition-smooth"
          >
            <Github className="mr-2 h-4 w-4" />
            Repository
          </Button>

          <Button
            variant="outline"
            className="border-border/50 hover:border-primary transition-smooth"
          >
            <Users className="mr-2 h-4 w-4" />
            {project.members} Members
          </Button>

          <Button
            variant="outline"
            size="icon"
            className="border-border/50 hover:border-primary transition-smooth"
          >
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="bg-muted/50 border border-border/50 p-1">
          <TabsTrigger
            value="notes"
            className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground transition-smooth"
          >
            <FileText className="mr-2 h-4 w-4" />
            Notes
          </TabsTrigger>
          <TabsTrigger
            value="tasks"
            className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground transition-smooth"
          >
            <ListTodo className="mr-2 h-4 w-4" />
            Tasks
          </TabsTrigger>
          <TabsTrigger
            value="docs"
            className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground transition-smooth"
          >
            <BookOpen className="mr-2 h-4 w-4" />
            Documentation
          </TabsTrigger>
        </TabsList>

        <TabsContent value="notes" className="space-y-4">
          <Card className="glass-card p-8 min-h-[400px] space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Project Notes</h2>
              <Button className="bg-primary hover:bg-primary/90" onClick={handleNewNote}>
                New Note
              </Button>
            </div>
            <div className="text-center py-12 text-muted-foreground">
              <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No notes yet. Create your first note to get started.</p>
            </div>
          </Card>
        </TabsContent>

        <TabsContent value="tasks" className="space-y-4">
          <Card className="glass-card p-8 min-h-[400px] space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Task Board</h2>
              <Button className="bg-secondary hover:bg-secondary/90" onClick={handleNewTask}>
                New Task
              </Button>
            </div>
            <div className="text-center py-12 text-muted-foreground">
              <ListTodo className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No tasks yet. Create your first task to organize work.</p>
            </div>
          </Card>
        </TabsContent>

        <TabsContent value="docs" className="space-y-4">
          <Card className="glass-card p-8 min-h-[400px] space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Documentation</h2>
              <Button className="bg-accent hover:bg-accent/90" onClick={handleNewDocument}>
                New Document
              </Button>
            </div>
            <div className="text-center py-12 text-muted-foreground">
              <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No documentation yet. Add your first document.</p>
            </div>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ProjectDetail;
