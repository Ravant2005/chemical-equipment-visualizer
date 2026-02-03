import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Clock, Trash2, Eye, Download } from 'lucide-react';
import { datasetAPI } from '../services/api';
import toast from 'react-hot-toast';
import Navbar from '../components/Navbar';
import AnimatedBackground from '../components/AnimatedBackground';

const History = () => {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await datasetAPI.getHistory();
      setDatasets(response.data);
    } catch (error) {
      toast.error('Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this dataset?')) return;
    
    try {
      await datasetAPI.delete(id);
      setDatasets(datasets.filter(d => d.id !== id));
      toast.success('Dataset deleted');
    } catch (error) {
      toast.error('Failed to delete dataset');
    }
  };

  const handleDownload = async (id) => {
    try {
      const token = localStorage.getItem('token');
      const url = `http://localhost:8000/api/datasets/${id}/generate_report/?token=${token}`;
      window.open(url, '_blank');
      toast.success('Report opened in new tab!');
    } catch (error) {
      toast.error('Failed to generate report');
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
            Upload History
          </h1>
          <p className="text-blue-300/70 text-lg">
            View and manage your last 5 uploaded datasets
          </p>
        </motion.div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-500 border-t-transparent"></div>
          </div>
        ) : datasets.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="glass-effect rounded-2xl p-12 text-center border border-white/10"
          >
            <Clock className="w-16 h-16 text-blue-400/50 mx-auto mb-4" />
            <p className="text-xl text-blue-300/70">No datasets uploaded yet</p>
          </motion.div>
        ) : (
          <div className="space-y-6">
            {datasets.map((dataset, index) => (
              <motion.div
                key={dataset.id}
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="glass-effect rounded-2xl p-6 border border-white/10 hover-lift"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-white mb-2">{dataset.filename}</h3>
                    <p className="text-blue-300/60 text-sm">
                      Uploaded: {new Date(dataset.uploaded_at).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex space-x-3">
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => handleDownload(dataset.id)}
                      className="p-3 rounded-lg bg-green-500/20 hover:bg-green-500/30 border border-green-500/30"
                    >
                      <Download className="w-5 h-5 text-green-400" />
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => handleDelete(dataset.id)}
                      className="p-3 rounded-lg bg-red-500/20 hover:bg-red-500/30 border border-red-500/30"
                    >
                      <Trash2 className="w-5 h-5 text-red-400" />
                    </motion.button>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <StatItem label="Total Equipment" value={dataset.total_count} />
                  <StatItem label="Avg Flowrate" value={dataset.avg_flowrate?.toFixed(2)} />
                  <StatItem label="Avg Pressure" value={dataset.avg_pressure?.toFixed(2)} />
                  <StatItem label="Avg Temperature" value={dataset.avg_temperature?.toFixed(2)} />
                </div>

                {dataset.equipment_distribution && (
                  <div className="mt-4 pt-4 border-t border-white/10">
                    <p className="text-sm text-blue-300/70 mb-2">Equipment Types:</p>
                    <div className="flex flex-wrap gap-2">
                      {Object.entries(dataset.equipment_distribution).map(([type, count]) => (
                        <span
                          key={type}
                          className="px-3 py-1 rounded-full glass-effect text-sm border border-white/20"
                        >
                          {type}: {count}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const StatItem = ({ label, value }) => (
  <div className="glass-effect rounded-lg p-3 border border-white/10">
    <p className="text-xs text-blue-300/60 mb-1">{label}</p>
    <p className="text-lg font-semibold">{value}</p>
  </div>
);

export default History;