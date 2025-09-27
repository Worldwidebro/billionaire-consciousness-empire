import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Play, 
  Pause, 
  Square, 
  RotateCcw, 
  Settings, 
  CheckCircle, 
  Clock, 
  AlertCircle,
  Zap,
  Brain,
  Target,
  TrendingUp,
  Users,
  DollarSign,
  Globe
} from 'lucide-react';

interface Workflow {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'paused' | 'completed' | 'error';
  progress: number;
  category: 'strategic' | 'operational' | 'financial' | 'expansion';
  priority: 'high' | 'medium' | 'low';
  estimatedDuration: string;
  actualDuration?: string;
  value: number;
  automation: boolean;
  steps: WorkflowStep[];
}

interface WorkflowStep {
  id: string;
  name: string;
  status: 'pending' | 'in-progress' | 'completed' | 'error';
  duration: string;
  automation: boolean;
  dependencies: string[];
}

export default function WorkflowUI() {
  const [workflows, setWorkflows] = useState<Workflow[]>([
    {
      id: '1',
      name: 'Billionaire Consciousness Expansion',
      description: 'Strategic expansion of consciousness-based business operations',
      status: 'active',
      progress: 75,
      category: 'strategic',
      priority: 'high',
      estimatedDuration: '30 days',
      actualDuration: '22 days',
      value: 13500000000,
      automation: true,
      steps: [
        { id: '1-1', name: 'Consciousness Assessment', status: 'completed', duration: '3 days', automation: true, dependencies: [] },
        { id: '1-2', name: 'Strategic Planning', status: 'completed', duration: '5 days', automation: false, dependencies: ['1-1'] },
        { id: '1-3', name: 'AI Integration', status: 'in-progress', duration: '7 days', automation: true, dependencies: ['1-2'] },
        { id: '1-4', name: 'Market Expansion', status: 'pending', duration: '10 days', automation: true, dependencies: ['1-3'] },
        { id: '1-5', name: 'Performance Optimization', status: 'pending', duration: '5 days', automation: true, dependencies: ['1-4'] }
      ]
    },
    {
      id: '2',
      name: 'Revenue Acceleration Pipeline',
      description: 'Automated revenue generation and optimization system',
      status: 'active',
      progress: 60,
      category: 'financial',
      priority: 'high',
      estimatedDuration: '21 days',
      actualDuration: '12 days',
      value: 8500000000,
      automation: true,
      steps: [
        { id: '2-1', name: 'Market Analysis', status: 'completed', duration: '2 days', automation: true, dependencies: [] },
        { id: '2-2', name: 'Client Acquisition', status: 'completed', duration: '4 days', automation: true, dependencies: ['2-1'] },
        { id: '2-3', name: 'Revenue Optimization', status: 'in-progress', duration: '6 days', automation: true, dependencies: ['2-2'] },
        { id: '2-4', name: 'Scaling Implementation', status: 'pending', duration: '7 days', automation: true, dependencies: ['2-3'] },
        { id: '2-5', name: 'Performance Monitoring', status: 'pending', duration: '2 days', automation: true, dependencies: ['2-4'] }
      ]
    },
    {
      id: '3',
      name: 'Global Market Penetration',
      description: 'Worldwide expansion and market dominance strategy',
      status: 'paused',
      progress: 40,
      category: 'expansion',
      priority: 'medium',
      estimatedDuration: '45 days',
      actualDuration: '18 days',
      value: 4200000000,
      automation: true,
      steps: [
        { id: '3-1', name: 'Market Research', status: 'completed', duration: '5 days', automation: true, dependencies: [] },
        { id: '3-2', name: 'Localization Setup', status: 'completed', duration: '8 days', automation: false, dependencies: ['3-1'] },
        { id: '3-3', name: 'Partnership Development', status: 'in-progress', duration: '12 days', automation: false, dependencies: ['3-2'] },
        { id: '3-4', name: 'Launch Execution', status: 'pending', duration: '15 days', automation: true, dependencies: ['3-3'] },
        { id: '3-5', name: 'Growth Optimization', status: 'pending', duration: '5 days', automation: true, dependencies: ['3-4'] }
      ]
    }
  ]);

  const [selectedWorkflow, setSelectedWorkflow] = useState<string | null>(null);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'paused': return 'bg-yellow-500';
      case 'completed': return 'bg-blue-500';
      case 'error': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-400';
      case 'medium': return 'text-yellow-400';
      case 'low': return 'text-green-400';
      default: return 'text-gray-400';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'strategic': return <Brain className="h-4 w-4" />;
      case 'operational': return <Zap className="h-4 w-4" />;
      case 'financial': return <DollarSign className="h-4 w-4" />;
      case 'expansion': return <Globe className="h-4 w-4" />;
      default: return <Target className="h-4 w-4" />;
    }
  };

  const getStepStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="h-4 w-4 text-green-400" />;
      case 'in-progress': return <Clock className="h-4 w-4 text-blue-400" />;
      case 'error': return <AlertCircle className="h-4 w-4 text-red-400" />;
      default: return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  const formatCurrency = (value: number) => {
    if (value >= 1000000000) {
      return `$${(value / 1000000000).toFixed(1)}B`;
    }
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`;
    }
    return `$${value.toLocaleString()}`;
  };

  const handleWorkflowAction = (workflowId: string, action: string) => {
    setWorkflows(prev => prev.map(workflow => {
      if (workflow.id === workflowId) {
        switch (action) {
          case 'play':
            return { ...workflow, status: 'active' };
          case 'pause':
            return { ...workflow, status: 'paused' };
          case 'stop':
            return { ...workflow, status: 'completed' };
          case 'reset':
            return { 
              ...workflow, 
              status: 'pending',
              progress: 0,
              steps: workflow.steps.map(step => ({ ...step, status: 'pending' }))
            };
          default:
            return workflow;
        }
      }
      return workflow;
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">
                Billionaire Workflow Orchestration
              </h1>
              <p className="text-xl text-blue-200">
                Strategic Process Management & Automation Control Center
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-green-400 border-green-400">
                <Zap className="h-4 w-4 mr-2" />
                {workflows.filter(w => w.status === 'active').length} Active
              </Badge>
              <Button variant="outline" className="text-white border-white hover:bg-white hover:text-black">
                <Settings className="h-4 w-4 mr-2" />
                Settings
              </Button>
            </div>
          </div>
        </div>

        {/* Workflow Overview */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-r from-green-600 to-green-700 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-200 text-sm font-medium">Active Workflows</p>
                  <p className="text-3xl font-bold text-white">
                    {workflows.filter(w => w.status === 'active').length}
                  </p>
                </div>
                <Play className="h-8 w-8 text-green-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-blue-600 to-blue-700 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-200 text-sm font-medium">Total Value</p>
                  <p className="text-3xl font-bold text-white">
                    {formatCurrency(workflows.reduce((sum, w) => sum + w.value, 0))}
                  </p>
                </div>
                <TrendingUp className="h-8 w-8 text-blue-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-purple-600 to-purple-700 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-200 text-sm font-medium">Automation Rate</p>
                  <p className="text-3xl font-bold text-white">
                    {Math.round((workflows.reduce((sum, w) => sum + (w.automation ? 1 : 0), 0) / workflows.length) * 100)}%
                  </p>
                </div>
                <Zap className="h-8 w-8 text-purple-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-orange-600 to-orange-700 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-orange-200 text-sm font-medium">Avg Progress</p>
                  <p className="text-3xl font-bold text-white">
                    {Math.round(workflows.reduce((sum, w) => sum + w.progress, 0) / workflows.length)}%
                  </p>
                </div>
                <Target className="h-8 w-8 text-orange-200" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Workflow Management */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="bg-gray-800/50">
            <TabsTrigger value="overview" className="text-white">Overview</TabsTrigger>
            <TabsTrigger value="details" className="text-white">Workflow Details</TabsTrigger>
            <TabsTrigger value="analytics" className="text-white">Analytics</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {workflows.map((workflow) => (
                <Card key={workflow.id} className="bg-gray-800/50 border-gray-700 hover:border-gray-600 transition-colors">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        {getCategoryIcon(workflow.category)}
                        <CardTitle className="text-white text-lg">{workflow.name}</CardTitle>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge 
                          variant="outline" 
                          className={`${getStatusColor(workflow.status)} text-white border-0`}
                        >
                          {workflow.status}
                        </Badge>
                        <span className={`text-sm ${getPriorityColor(workflow.priority)}`}>
                          {workflow.priority}
                        </span>
                      </div>
                    </div>
                    <p className="text-gray-300 text-sm">{workflow.description}</p>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-gray-300">Progress</span>
                        <span className="text-white font-medium">{workflow.progress}%</span>
                      </div>
                      <Progress value={workflow.progress} className="h-2" />
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-400">Value:</span>
                        <p className="text-white font-medium">{formatCurrency(workflow.value)}</p>
                      </div>
                      <div>
                        <span className="text-gray-400">Duration:</span>
                        <p className="text-white font-medium">{workflow.estimatedDuration}</p>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-1">
                        <Zap className="h-4 w-4 text-yellow-400" />
                        <span className="text-sm text-gray-300">
                          {workflow.automation ? 'Automated' : 'Manual'}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={() => handleWorkflowAction(workflow.id, workflow.status === 'active' ? 'pause' : 'play')}
                          className="text-white border-white hover:bg-white hover:text-black"
                        >
                          {workflow.status === 'active' ? <Pause className="h-3 w-3" /> : <Play className="h-3 w-3" />}
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={() => setSelectedWorkflow(workflow.id)}
                          className="text-white border-white hover:bg-white hover:text-black"
                        >
                          Details
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="details" className="space-y-6">
            {selectedWorkflow ? (
              (() => {
                const workflow = workflows.find(w => w.id === selectedWorkflow);
                if (!workflow) return null;
                
                return (
                  <Card className="bg-gray-800/50 border-gray-700">
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <div>
                          <CardTitle className="text-white text-2xl">{workflow.name}</CardTitle>
                          <p className="text-gray-300 mt-2">{workflow.description}</p>
                        </div>
                        <div className="flex items-center space-x-4">
                          <Button 
                            variant="outline"
                            onClick={() => handleWorkflowAction(workflow.id, workflow.status === 'active' ? 'pause' : 'play')}
                            className="text-white border-white hover:bg-white hover:text-black"
                          >
                            {workflow.status === 'active' ? <Pause className="h-4 w-4 mr-2" /> : <Play className="h-4 w-4 mr-2" />}
                            {workflow.status === 'active' ? 'Pause' : 'Start'}
                          </Button>
                          <Button 
                            variant="outline"
                            onClick={() => handleWorkflowAction(workflow.id, 'reset')}
                            className="text-white border-white hover:bg-white hover:text-black"
                          >
                            <RotateCcw className="h-4 w-4 mr-2" />
                            Reset
                          </Button>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div>
                          <h3 className="text-white font-medium mb-3">Workflow Steps</h3>
                          <div className="space-y-3">
                            {workflow.steps.map((step) => (
                              <div key={step.id} className="flex items-center space-x-3 p-3 bg-gray-700/50 rounded-lg">
                                {getStepStatusIcon(step.status)}
                                <div className="flex-1">
                                  <p className="text-white text-sm font-medium">{step.name}</p>
                                  <p className="text-gray-400 text-xs">{step.duration}</p>
                                </div>
                                <div className="flex items-center space-x-1">
                                  {step.automation && <Zap className="h-3 w-3 text-yellow-400" />}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div>
                          <h3 className="text-white font-medium mb-3">Progress Overview</h3>
                          <div className="space-y-4">
                            <div>
                              <div className="flex justify-between text-sm mb-2">
                                <span className="text-gray-300">Overall Progress</span>
                                <span className="text-white font-medium">{workflow.progress}%</span>
                              </div>
                              <Progress value={workflow.progress} className="h-3" />
                            </div>
                            <div className="space-y-2">
                              <div className="flex justify-between text-sm">
                                <span className="text-gray-300">Completed Steps</span>
                                <span className="text-green-400">
                                  {workflow.steps.filter(s => s.status === 'completed').length}/{workflow.steps.length}
                                </span>
                              </div>
                              <div className="flex justify-between text-sm">
                                <span className="text-gray-300">Estimated Duration</span>
                                <span className="text-white">{workflow.estimatedDuration}</span>
                              </div>
                              <div className="flex justify-between text-sm">
                                <span className="text-gray-300">Actual Duration</span>
                                <span className="text-white">{workflow.actualDuration || 'In Progress'}</span>
                              </div>
                            </div>
                          </div>
                        </div>

                        <div>
                          <h3 className="text-white font-medium mb-3">Workflow Metrics</h3>
                          <div className="space-y-4">
                            <div className="p-4 bg-gray-700/50 rounded-lg">
                              <div className="flex items-center justify-between mb-2">
                                <span className="text-gray-300 text-sm">Total Value</span>
                                <span className="text-white font-medium">{formatCurrency(workflow.value)}</span>
                              </div>
                            </div>
                            <div className="p-4 bg-gray-700/50 rounded-lg">
                              <div className="flex items-center justify-between mb-2">
                                <span className="text-gray-300 text-sm">Automation Level</span>
                                <span className="text-white font-medium">
                                  {Math.round((workflow.steps.filter(s => s.automation).length / workflow.steps.length) * 100)}%
                                </span>
                              </div>
                            </div>
                            <div className="p-4 bg-gray-700/50 rounded-lg">
                              <div className="flex items-center justify-between mb-2">
                                <span className="text-gray-300 text-sm">Priority</span>
                                <Badge variant="outline" className={getPriorityColor(workflow.priority)}>
                                  {workflow.priority}
                                </Badge>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                );
              })()
            ) : (
              <Card className="bg-gray-800/50 border-gray-700">
                <CardContent className="p-12 text-center">
                  <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-white text-xl mb-2">Select a Workflow</h3>
                  <p className="text-gray-400">Choose a workflow from the overview to view detailed information and manage its execution.</p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-gray-800/50 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white">Workflow Performance</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center text-gray-400">
                    Performance Chart Component
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gray-800/50 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white">Automation Efficiency</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center text-gray-400">
                    Efficiency Chart Component
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
