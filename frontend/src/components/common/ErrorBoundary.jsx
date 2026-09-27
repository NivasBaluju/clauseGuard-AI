import React from "react";
import { AlertTriangle, RotateCcw } from "lucide-react";

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[400px] flex flex-col items-center justify-center p-8 text-center bg-white">
          <div className="w-12 h-12 rounded-xl bg-red-50 border border-red-200 text-red-600 flex items-center justify-center mb-4">
            <AlertTriangle size={24} />
          </div>
          <h2 className="text-lg font-bold text-neutral-900 mb-2 font-serif">
            Something unexpected occurred
          </h2>
          <p className="text-sm text-neutral-600 max-w-md mb-6 leading-relaxed">
            The workspace encountered a temporary rendering issue. Please reload to restore your session.
          </p>
          <button
            onClick={this.handleReset}
            className="inline-flex items-center gap-2 px-4 py-2 bg-black text-white text-xs font-mono font-medium rounded hover:bg-neutral-800 transition-colors"
          >
            <RotateCcw size={14} />
            Reload Workspace
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
