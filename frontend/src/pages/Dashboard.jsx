import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, Download, TrendingUp, Activity, Thermometer, Gauge } from 'lucide-react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, LineElement, PointElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar, Line, Pie } from 'react-chartjs-2';
import { datasetAPI } from '../services/api';
import toast from 'react-hot-toast';
import Navbar from '../components/Navbar';
import AnimatedBackground from '../components/AnimatedBackground';

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, ArcElement, Title, Tooltip, Legend);

const Dashboard = () => {
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    try {
      const response = await datasetAPI.upload(file);
      setDataset(response.data);
      toast.success('File uploaded successfully!');
    } catch (error) {
      toast.error(error.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!dataset) return;
    
    try {
      const token = localStorage.getItem('token');
      const apiBase = import.meta.env.VITE_API_URL || 'https://your-backend.railway.app';
      const url = `${apiBase}/api/datasets/${dataset.id}/generate_report/?token=${token}`;
      window.open(url, '_blank');
      toast.success('Report opened in new tab!');
    } catch (error) {
      console.error('Report generation error:', error);
      toast.error('Failed to generate report');
    }
  };

  // Chart data
  const equipmentDistribution = dataset?.equipment_distribution || {};
  const pieData = {
    labels: Object.keys(equipmentDistribution),
    datasets: [{
      data: Object.values(equipmentDistribution),
      backgroundColor: [
        'rgba(59, 130, 246, 0.8)',
        'rgba(139, 92, 246, 0.8)',
        'rgba(236, 72, 153, 0.8)',
        'rgba(251, 146, 60, 0.8)',
        'rgba(34, 197, 94, 0.8)',
      ],
      borderColor: 'rgba(255, 255, 255, 0.2)',
      borderWidth: 2,
    }]
  };

  const barData = {
    labels: dataset?.equipment?.map(e => e.equipment_name) || [],
    datasets: [{
      label: 'Flowrate',
      data: dataset?.equipment?.map(e => e.flowrate) || [],
      backgroundColor: 'rgba(59, 130, 246, 0.6)',
    }, {
      label: 'Pressure',
      data: dataset?.equipment?.map(e => e.pressure) || [],
      backgroundColor: 'rgba(139, 92, 246, 0.6)',
    }, {
      label: 'Temperature',
      data: dataset?.equipment?.map(e => e.temperature) || [],
      backgroundColor: 'rgba(236, 72, 153, 0.6)',
    }]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: { color: 'rgba(255, 255, 255, 0.8)' }
      }
    },
    scales: {
      x: { ticks: { color: 'rgba(255, 255, 255, 0.6)' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
      y: { ticks: { color: 'rgba(255, 255, 255, 0.6)' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } }
    }
  };

  return (
    <div className="min-h-screen relative">
      <AnimatedBackground />
      <Navbar />
      
      <div className="container mx-auto px-6 pt-24 pb-12 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-5xl font-display font-bold text-gradient mb-3">
            Equipment Analytics Dashboard
          </h1>
          <p className="text-blue-300/70 text-lg">
            Upload CSV files and visualize chemical equipment data in real-time
          </p>
        </motion.div>

        {/* Upload Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-12"
        >
          <div className="glass-morphism rounded-2xl p-8 border border-white/10 hover-lift chemical-container relative overflow-hidden">
            {/* Animated background elements */}
            <div className="absolute inset-0 opacity-20">
              <div className="absolute top-4 left-4 w-8 h-8 border-2 border-blue-400 rounded-full animate-pulse" />
              <div className="absolute top-8 right-8 w-6 h-6 border-2 border-purple-400 rounded-full animate-pulse" style={{ animationDelay: '0.5s' }} />
              <div className="absolute bottom-6 left-12 w-4 h-4 border-2 border-pink-400 rounded-full animate-pulse" style={{ animationDelay: '1s' }} />
            </div>
            
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              className="hidden"
            />
            <motion.button
              whileHover={{ scale: 1.02, rotateY: 2 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
              className="w-full py-8 rounded-xl bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 hover:from-blue-500 hover:via-purple-500 hover:to-pink-500 font-semibold text-lg glow-effect button-glow flex items-center justify-center space-x-3 disabled:opacity-50 relative overflow-hidden"
              style={{ transformStyle: 'preserve-3d' }}
            >
              <motion.div
                animate={uploading ? { rotate: 360 } : { rotate: 0 }}
                transition={{ duration: 1, repeat: uploading ? Infinity : 0, ease: "linear" }}
              >
                <Upload className="w-7 h-7" />
              </motion.div>
              <span className="relative z-10">{uploading ? 'Processing Chemical Data...' : 'Upload Chemical Equipment CSV'}</span>
              {!uploading && (
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
              )}
            </motion.button>
            
            {/* Chemical formula decorations */}
            <div className="absolute top-2 right-2 text-xs text-blue-300/30 chemical-formula">C₆H₁₂O₆</div>
            <div className="absolute bottom-2 left-2 text-xs text-purple-300/30 chemical-formula">H₂SO₄</div>
          </div>
        </motion.div>

        {/* Statistics Cards */}
        {dataset && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12"
          >
            <StatsCard icon={FileText} title="Total Equipment" value={dataset.total_count} color="blue" />
            <StatsCard icon={Activity} title="Avg Flowrate" value={dataset.avg_flowrate?.toFixed(2)} color="purple" />
            <StatsCard icon={Gauge} title="Avg Pressure" value={dataset.avg_pressure?.toFixed(2)} color="pink" />
            <StatsCard icon={Thermometer} title="Avg Temperature" value={dataset.avg_temperature?.toFixed(2)} color="orange" />
          </motion.div>
        )}

        {/* Charts */}
        {dataset && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <ChartCard title="Equipment Distribution">
                <Pie data={pieData} options={{ ...chartOptions, maintainAspectRatio: true }} />
              </ChartCard>
              <ChartCard title="Parameter Comparison">
                <div className="h-80">
                  <Bar data={barData} options={chartOptions} />
                </div>
              </ChartCard>
            </div>

            {/* Download Report */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleDownloadReport}
              className="w-full py-4 rounded-xl bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 font-semibold text-lg glow-effect button-glow flex items-center justify-center space-x-3"
            >
              <Download className="w-6 h-6" />
              <span>Generate PDF Report</span>
            </motion.button>
          </>
        )}
      </div>
    </div>
  );
};

const StatsCard = ({ icon: Icon, title, value, color }) => {
  const colors = {
    blue: 'from-blue-600 to-blue-400',
    purple: 'from-purple-600 to-purple-400',
    pink: 'from-pink-600 to-pink-400',
    orange: 'from-orange-600 to-orange-400',
  };

  return (
    <motion.div
      whileHover={{ y: -8, rotateY: 5, rotateX: 5 }}
      whileTap={{ scale: 0.95 }}
      className="glass-morphism rounded-2xl p-6 border border-white/10 hover-lift interactive-element chemical-container"
      style={{ transformStyle: 'preserve-3d' }}
    >
      <motion.div
        className={`w-16 h-16 rounded-xl bg-gradient-to-br ${colors[color]} flex items-center justify-center mb-4 glow-effect molecule-3d`}
        whileHover={{ scale: 1.1, rotateZ: 180 }}
        transition={{ duration: 0.3 }}
      >
        <Icon className="w-8 h-8 text-white" />
      </motion.div>
      <p className="text-blue-300/70 text-sm mb-1">{title}</p>
      <motion.p 
        className="text-3xl font-bold text-gradient"
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
      >
        {value}
      </motion.p>
      <div className="absolute inset-0 rounded-2xl shimmer opacity-0 hover:opacity-100 transition-opacity duration-300" />
    </motion.div>
  );
};

const ChartCard = ({ title, children }) => (
  <motion.div
    initial={{ opacity: 0, y: 20, rotateX: -15 }}
    animate={{ opacity: 1, y: 0, rotateX: 0 }}
    whileHover={{ y: -5, rotateY: 2, rotateX: 2 }}
    className="glass-morphism rounded-2xl p-6 border border-white/10 hover-lift chemical-container"
    style={{ transformStyle: 'preserve-3d' }}
  >
    <div className="relative">
      <h3 className="text-xl font-semibold mb-6 text-gradient chemical-formula">{title}</h3>
      <div className="relative z-10">
        {children}
      </div>
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-blue-500/10 to-purple-500/10 opacity-0 hover:opacity-100 transition-opacity duration-500" />
      <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-blue-400/20 to-transparent rounded-full blur-xl" />
    </div>
  </motion.div>
);

export default Dashboard;