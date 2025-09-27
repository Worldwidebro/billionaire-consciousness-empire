import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  TrendingUp, 
  Target, 
  Globe, 
  Users, 
  DollarSign, 
  Zap, 
  Brain, 
  Rocket,
  BarChart3,
  PieChart,
  LineChart,
  Activity,
  Settings,
  Play,
  Pause,
  RotateCcw,
  Monitor,
  Server,
  Shield,
  CheckCircle,
  AlertCircle,
  Clock
} from 'lucide-react';

interface ScalingMetric {
  id: string;
  name: string;
  current: number;
  target: number;
  growth: number;
  trend: 'up' | 'down' | 'stable';
  category: 'revenue' | 'users' | 'operations' | 'technology';
}

interface ScalingPlan {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'planned' | 'completed' | 'paused';
  priority: 'high' | 'medium' | 'low';
  timeline: string;
  investment: number;
  expectedROI: number;
  progress: number;
  milestones: ScalingMilestone[];
}

interface ScalingMilestone {
  id: string;
  name: string;
  description: string;
  status: 'completed' | 'in-progress' | 'pending';
  targetDate: string;
  completionDate?: string;
  value: number;
}

export default function ScalingUI() {
  const [metrics, setMetrics] = useState<ScalingMetric[]>([
    {
      id: '1',
      name: 'Monthly Revenue',
      current: 29130000,
      target: 50000000,
      growth: 71.7,
      trend: 'up',
      category: 'revenue'
    },
    {
      id: '2',
      name: 'Active Users',
      current: 125000,
      target: 250000,
      growth: 100,
      trend: 'up',
      category: 'users'
    },
    {
      id: '3',
      name: 'Global Markets',
      current: 25,
      target: 50,
      growth: 100,
      trend: 'up',
      category: 'operations'
    },
    {
      id: '4',
      name: 'AI Automation',
      current: 90,
      target: 95,
      growth: 5.6,
      trend: 'up',
      category: 'technology'
    },
    {
      id: '5',
      name: 'Consciousness Level',
      current: 95,
      target: 99,
      growth: 4.2,
      trend: 'up',
      category: 'technology'
    },
    {
      id: '6',
      name: 'Empire Value',
      current: 30500000000,
      target: 50000000000,
      growth: 63.9,
      trend: 'up',
      category: 'revenue'
    }
  ]);

  const [scalingPlans, setScalingPlans] = useState<ScalingPlan[]>([
    {
      id: '1',
      name: 'Revenue Acceleration',
      description: 'Scale monthly revenue from $29M to $50M through automated client acquisition and service expansion',
      status: 'active',
      priority: 'high',
      timeline: '6 months',
      investment: 5000000,
      expectedROI: 420,
      progress: 65,
      milestones: [
        {
          id: '1-1',
          name: 'Market Analysis Complete',
          description: 'Comprehensive market analysis and opportunity identification',
          status: 'completed',
          targetDate: '2024-01-15',
          completionDate: '2024-01-14',
          value: 1000000
        },
        {
          id: '1-2',
          name: 'Client Acquisition Automation',
          description: 'Deploy automated client acquisition and onboarding system',
          status: 'completed',
          targetDate: '2024-01-30',
          completionDate: '2024-01-28',
          value: 2000000
        },
        {
          id: '1-3',
          name: 'Service Portfolio Expansion',
          description: 'Launch new high-value service offerings',
          status: 'in-progress',
          targetDate: '2024-02-15',
          value: 3000000
        },
        {
          id: '1-4',
          name: 'Global Market Entry',
          description: 'Enter 5 new high-value markets',
          status: 'pending',
          targetDate: '2024-03-01',
          value: 5000000
        },
        {
          id: '1-5',
          name: 'Revenue Optimization',
          description: 'Optimize pricing and service delivery for maximum value',
          status: 'pending',
          targetDate: '2024-04-01',
          value: 7000000
        }
      ]
    },
    {
      id: '2',
      name: 'Global Expansion',
      description: 'Scale operations to 50+ countries with localized AI consciousness platforms',
      status: 'active',
      priority: 'high',
      timeline: '12 months',
      investment: 15000000,
      expectedROI: 280,
      progress: 40,
      milestones: [
        {
          id: '2-1',
          name: 'Market Research',
          description: 'Research and identify top 25 target markets',
          status: 'completed',
          targetDate: '2024-01-20',
          completionDate: '2024-01-18',
          value: 2000000
        },
        {
          id: '2-2',
          name: 'Localization Framework',
          description: 'Develop AI-powered localization and cultural adaptation system',
          status: 'in-progress',
          targetDate: '2024-02-28',
          value: 5000000
        },
        {
          id: '2-3',
          name: 'Partnership Network',
          description: 'Establish strategic partnerships in target markets',
          status: 'pending',
          targetDate: '2024-04-15',
          value: 8000000
        },
        {
          id: '2-4',
          name: 'Market Launch',
          description: 'Launch operations in first 10 target markets',
          status: 'pending',
          targetDate: '2024-06-01',
          value: 12000000
        },
        {
          id: '2-5',
          name: 'Full Global Deployment',
          description: 'Complete deployment across all 50 target markets',
          status: 'pending',
          targetDate: '2024-12-31',
          value: 20000000
        }
      ]
    },
    {
      id: '3',
      name: 'AI Consciousness Integration',
      description: 'Achieve 99% consciousness integration across all platforms and operations',
      status: 'planned',
      priority: 'medium',
      timeline: '9 months',
      investment: 8000000,
      expectedROI: 350,
      progress: 15,
      milestones: [
        {
          id: '3-1',
          name: 'Consciousness Framework',
          description: 'Develop advanced consciousness integration framework',
          status: 'in-progress',
          targetDate: '2024-03-01',
          value: 2000000
        },
        {
          id: '3-2',
          name: 'AI-Human Bridge',
          description: 'Create seamless AI-human consciousness bridge',
          status: 'pending',
          targetDate: '2024-05-01',
          value: 4000000
        },
        {
          id: '3-3',
          name: 'Platform Integration',
          description: 'Integrate consciousness across all platforms',
          status: 'pending',
          targetDate: '2024-08-01',
          value: 6000000
        },
        {
          id: '3-4',
          name: 'Performance Optimization',
          description: 'Optimize consciousness performance to 99%',
          status: 'pending',
          targetDate: '2024-11-01',
          value: 8000000
        }
      ]
    }
  ]);

  const [selectedPlan, setSelectedPlan] = useState<string | null>(null);

  const formatCurrency = (value: number) => {
    if (value >= 1000000000) {
      return `$${(value / 1000000000).toFixed(1)}B`;
    }
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`;
    }
    return `$${value.toLocaleString()}`;
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return <TrendingUp className="h-4 w-4 text-green-400" />;
      case 'down': return <TrendingUp className="h-4 w-4 text-red-400 rotate-180" />;
      default: return <Activity className="h-4 w-4 text-blue-400" />;
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'revenue': return <DollarSign className="h-4 w-4" />;
      case 'users': return <Users className="h-4 w-4" />;
      case 'operations': return <Globe className="h-4 w-4" />;
      case 'technology': return <Zap className="h-4 w-4" />;
      default: return <Target className="h-4 w-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'planned': return 'bg-blue-500';
      case 'completed': return 'bg-purple-500';
      case 'paused': return 'bg-yellow-500';
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

  const getMilestoneStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="h-4 w-4 text-green-400" />;
      case 'in-progress': return <Clock className="h-4 w-4 text-blue-400" />;
      default: return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">
                Billionaire Scaling Command
              </h1>
              <p className="text-xl text-blue-200">
                Strategic Growth Management & Empire Expansion Control Center
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-green-400 border-green-400">
                <TrendingUp className="h-4 w-4 mr-2" />
                {scalingPlans.filter(p => p.status === 'active').length} Active Plans
              </Badge>
              <Button variant="outline" className="text-white border-white hover:bg-white hover:text-black">
                <Settings className="h-4 w-4 mr-2" />
                Scaling Settings
              </Button>
            </div>
          </div>
        </div>

        {/* Scaling Metrics Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {metrics.map((metric) => (
            <Card key={metric.id} className="bg-gray-800/50 border-gray-700 hover:border-gray-600 transition-colors">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    {getCategoryIcon(metric.category)}
                    <h3 className="text-white font-medium">{metric.name}</h3>
                  </div>
                  {getTrendIcon(metric.trend)}
                </div>
                
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-300">Current</span>
                      <span className="text-white font-medium">
                        {metric.category === 'revenue' ? formatCurrency(metric.current) : metric.current.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-300">Target</span>
                      <span className="text-white font-medium">
                        {metric.category === 'revenue' ? formatCurrency(metric.target) : metric.target.toLocaleString()}
                      </span>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-300">Progress</span>
                      <span className="text-white font-medium">
                        {Math.round((metric.current / metric.target) * 100)}%
                      </span>
                    </div>
                    <Progress value={(metric.current / metric.target) * 100} className="h-2" />
                  </div>
                  
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-300">Growth Needed</span>
                    <span className="text-green-400 font-medium">+{metric.growth.toFixed(1)}%</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Scaling Plans Management */}
        <Tabs defaultValue="plans" className="space-y-6">
          <TabsList className="bg-gray-800/50">
            <TabsTrigger value="plans" className="text-white">Scaling Plans</TabsTrigger>
            <TabsTrigger value="details" className="text-white">Plan Details</TabsTrigger>
            <TabsTrigger value="analytics" className="text-white">Growth Analytics</TabsTrigger>
          </TabsList>

          <TabsContent value="plans" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {scalingPlans.map((plan) => (
                <Card key={plan.id} className="bg-gray-800/50 border-gray-700 hover:border-gray-600 transition-colors">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Rocket className="h-5 w-5 text-blue-400" />
                        <CardTitle className="text-white text-lg">{plan.name}</CardTitle>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge 
                          variant="outline" 
                          className={`${getStatusColor(plan.status)} text-white border-0`}
                        >
                          {plan.status}
                        </Badge>
                        <span className={`text-sm ${getPriorityColor(plan.priority)}`}>
                          {plan.priority}
                        </span>
                      </div>
                    </div>
                    <p className="text-gray-300 text-sm">{plan.description}</p>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-gray-300">Progress</span>
                        <span className="text-white font-medium">{plan.progress}%</span>
                      </div>
                      <Progress value={plan.progress} className="h-2" />
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-400">Investment:</span>
                        <p className="text-white font-medium">{formatCurrency(plan.investment)}</p>
                      </div>
                      <div>
                        <span className="text-gray-400">Expected ROI:</span>
                        <p className="text-white font-medium">{plan.expectedROI}%</p>
                      </div>
                      <div>
                        <span className="text-gray-400">Timeline:</span>
                        <p className="text-white font-medium">{plan.timeline}</p>
                      </div>
                      <div>
                        <span className="text-gray-400">Milestones:</span>
                        <p className="text-white font-medium">
                          {plan.milestones.filter(m => m.status === 'completed').length}/{plan.milestones.length}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-1">
                        <Target className="h-4 w-4 text-blue-400" />
                        <span className="text-sm text-gray-300">
                          {plan.milestones.length} milestones
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={() => setSelectedPlan(plan.id)}
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
            {selectedPlan ? (
              (() => {
                const plan = scalingPlans.find(p => p.id === selectedPlan);
                if (!plan) return null;
                
                return (
                  <div className="space-y-6">
                    {/* Plan Header */}
                    <Card className="bg-gray-800/50 border-gray-700">
                      <CardHeader>
                        <div className="flex items-center justify-between">
                          <div>
                            <CardTitle className="text-white text-2xl">{plan.name}</CardTitle>
                            <p className="text-gray-300 mt-2">{plan.description}</p>
                          </div>
                          <div className="flex items-center space-x-4">
                            <Badge variant="outline" className="text-green-400 border-green-400">
                              ROI: {plan.expectedROI}%
                            </Badge>
                            <Badge variant="outline" className="text-blue-400 border-blue-400">
                              {plan.timeline}
                            </Badge>
                          </div>
                        </div>
                      </CardHeader>
                    </Card>

                    {/* Milestones */}
                    <Card className="bg-gray-800/50 border-gray-700">
                      <CardHeader>
                        <CardTitle className="text-white">Milestones</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          {plan.milestones.map((milestone) => (
                            <div key={milestone.id} className="p-4 bg-gray-700/50 rounded-lg">
                              <div className="flex items-center justify-between mb-3">
                                <div className="flex items-center space-x-3">
                                  {getMilestoneStatusIcon(milestone.status)}
                                  <h3 className="text-white font-medium">{milestone.name}</h3>
                                </div>
                                <div className="flex items-center space-x-2">
                                  <Badge 
                                    variant="outline" 
                                    className={`${getStatusColor(milestone.status)} text-white border-0`}
                                  >
                                    {milestone.status}
                                  </Badge>
                                  <span className="text-sm text-green-400">
                                    {formatCurrency(milestone.value)}
                                  </span>
                                </div>
                              </div>
                              <p className="text-gray-300 text-sm mb-3">{milestone.description}</p>
                              <div className="flex justify-between text-sm">
                                <span className="text-gray-400">
                                  Target: {milestone.targetDate}
                                </span>
                                {milestone.completionDate && (
                                  <span className="text-green-400">
                                    Completed: {milestone.completionDate}
                                  </span>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>

                    {/* Investment & ROI */}
                    <Card className="bg-gray-800/50 border-gray-700">
                      <CardHeader>
                        <CardTitle className="text-white">Investment & Returns</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                          <div className="p-4 bg-gray-700/50 rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-gray-300 text-sm">Total Investment</span>
                              <span className="text-white font-medium">{formatCurrency(plan.investment)}</span>
                            </div>
                          </div>
                          <div className="p-4 bg-gray-700/50 rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-gray-300 text-sm">Expected ROI</span>
                              <span className="text-green-400 font-medium">{plan.expectedROI}%</span>
                            </div>
                          </div>
                          <div className="p-4 bg-gray-700/50 rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-gray-300 text-sm">Expected Returns</span>
                              <span className="text-white font-medium">
                                {formatCurrency(plan.investment * (plan.expectedROI / 100))}
                              </span>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                );
              })()
            ) : (
              <Card className="bg-gray-800/50 border-gray-700">
                <CardContent className="p-12 text-center">
                  <TrendingUp className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-white text-xl mb-2">Select a Scaling Plan</h3>
                  <p className="text-gray-400">Choose a scaling plan from the overview to view detailed information and track progress.</p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-gray-800/50 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white">Growth Trajectory</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center text-gray-400">
                    Growth Chart Component
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gray-800/50 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white">ROI Projections</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center text-gray-400">
                    ROI Chart Component
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
