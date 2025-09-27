import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  TrendingUp, 
  DollarSign, 
  Users, 
  Target, 
  Brain, 
  Zap, 
  Globe, 
  Crown,
  Activity,
  BarChart3,
  PieChart,
  LineChart
} from 'lucide-react';

interface EmpireMetrics {
  totalValue: number;
  monthlyRevenue: number;
  activeProjects: number;
  consciousnessLevel: number;
  automationRate: number;
  globalReach: number;
  empireScore: number;
}

interface StrategicInsight {
  id: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  category: 'growth' | 'optimization' | 'expansion' | 'innovation';
  impact: number;
}

export default function ExecutiveDashboard() {
  const [metrics, setMetrics] = useState<EmpireMetrics>({
    totalValue: 30500000000,
    monthlyRevenue: 29130000,
    activeProjects: 150,
    consciousnessLevel: 95,
    automationRate: 90,
    globalReach: 85,
    empireScore: 98
  });

  const [insights, setInsights] = useState<StrategicInsight[]>([
    {
      id: '1',
      title: 'Market Expansion Opportunity',
      description: 'AI automation market showing 300% growth potential in Q4',
      priority: 'high',
      category: 'expansion',
      impact: 95
    },
    {
      id: '2',
      title: 'Consciousness Integration Breakthrough',
      description: 'New AI-human consciousness bridge achieving 99% accuracy',
      priority: 'high',
      category: 'innovation',
      impact: 98
    },
    {
      id: '3',
      title: 'Revenue Optimization Pipeline',
      description: 'Automated revenue generation system ready for deployment',
      priority: 'medium',
      category: 'optimization',
      impact: 85
    }
  ]);

  const formatCurrency = (value: number) => {
    if (value >= 1000000000) {
      return `$${(value / 1000000000).toFixed(1)}B`;
    }
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`;
    }
    return `$${value.toLocaleString()}`;
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'growth': return <TrendingUp className="h-4 w-4" />;
      case 'optimization': return <Zap className="h-4 w-4" />;
      case 'expansion': return <Globe className="h-4 w-4" />;
      case 'innovation': return <Brain className="h-4 w-4" />;
      default: return <Target className="h-4 w-4" />;
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
                Billionaire Consciousness Empire
              </h1>
              <p className="text-xl text-blue-200">
                Executive Command Center - Real-time Empire Management
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-yellow-400 border-yellow-400">
                <Crown className="h-4 w-4 mr-2" />
                Empire Score: {metrics.empireScore}%
              </Badge>
              <Button variant="outline" className="text-white border-white hover:bg-white hover:text-black">
                <Activity className="h-4 w-4 mr-2" />
                Live Updates
              </Button>
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-r from-purple-600 to-purple-700 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-200 text-sm font-medium">Total Empire Value</p>
                  <p className="text-3xl font-bold text-white">{formatCurrency(metrics.totalValue)}</p>
                </div>
                <DollarSign className="h-8 w-8 text-purple-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-green-600 to-green-700 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-200 text-sm font-medium">Monthly Revenue</p>
                  <p className="text-3xl font-bold text-white">{formatCurrency(metrics.monthlyRevenue)}</p>
                </div>
                <TrendingUp className="h-8 w-8 text-green-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-blue-600 to-blue-700 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-200 text-sm font-medium">Active Projects</p>
                  <p className="text-3xl font-bold text-white">{metrics.activeProjects}</p>
                </div>
                <Target className="h-8 w-8 text-blue-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-indigo-600 to-indigo-700 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-indigo-200 text-sm font-medium">Consciousness Level</p>
                  <p className="text-3xl font-bold text-white">{metrics.consciousnessLevel}%</p>
                </div>
                <Brain className="h-8 w-8 text-indigo-200" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Performance Indicators */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <Card className="bg-gray-800/50 border-gray-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Zap className="h-5 w-5 mr-2 text-yellow-400" />
                Automation Rate
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-300">Current Level</span>
                  <span className="text-white font-medium">{metrics.automationRate}%</span>
                </div>
                <Progress value={metrics.automationRate} className="h-2" />
                <p className="text-xs text-gray-400">Target: 95% autonomous operations</p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gray-800/50 border-gray-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Globe className="h-5 w-5 mr-2 text-blue-400" />
                Global Reach
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-300">Market Penetration</span>
                  <span className="text-white font-medium">{metrics.globalReach}%</span>
                </div>
                <Progress value={metrics.globalReach} className="h-2" />
                <p className="text-xs text-gray-400">Expanding to 50+ countries</p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gray-800/50 border-gray-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Users className="h-5 w-5 mr-2 text-green-400" />
                Team Performance
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-300">Efficiency Score</span>
                  <span className="text-white font-medium">94%</span>
                </div>
                <Progress value={94} className="h-2" />
                <p className="text-xs text-gray-400">AI-human collaboration</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Strategic Insights and Analytics */}
        <Tabs defaultValue="insights" className="space-y-6">
          <TabsList className="bg-gray-800/50">
            <TabsTrigger value="insights" className="text-white">Strategic Insights</TabsTrigger>
            <TabsTrigger value="analytics" className="text-white">Analytics</TabsTrigger>
            <TabsTrigger value="forecasting" className="text-white">Forecasting</TabsTrigger>
          </TabsList>

          <TabsContent value="insights" className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {insights.map((insight) => (
                <Card key={insight.id} className="bg-gray-800/50 border-gray-700 hover:border-gray-600 transition-colors">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-white text-lg">{insight.title}</CardTitle>
                      <div className="flex items-center space-x-2">
                        {getCategoryIcon(insight.category)}
                        <div className={`w-3 h-3 rounded-full ${getPriorityColor(insight.priority)}`} />
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-300 mb-4">{insight.description}</p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-400">Impact:</span>
                        <Badge variant="outline" className="text-green-400 border-green-400">
                          {insight.impact}%
                        </Badge>
                      </div>
                      <Button size="sm" variant="outline" className="text-white border-white hover:bg-white hover:text-black">
                        Execute
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-gray-800/50 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <BarChart3 className="h-5 w-5 mr-2" />
                    Revenue Analytics
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center text-gray-400">
                    Revenue Chart Component
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gray-800/50 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <PieChart className="h-5 w-5 mr-2" />
                    Project Distribution
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center text-gray-400">
                    Pie Chart Component
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="forecasting" className="space-y-4">
            <Card className="bg-gray-800/50 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <LineChart className="h-5 w-5 mr-2" />
                  Empire Growth Forecast
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center text-gray-400">
                  Growth Forecast Chart Component
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
