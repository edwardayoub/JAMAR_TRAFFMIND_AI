import React from "react"
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"

class LineDrawing extends StreamlitComponentBase {
  constructor(props) {
    super(props)
    this.state = {
      image: this.props.args["image"],
      width: this.props.args["width"],
      height: this.props.args["height"],
      lines: this.props.args["lines"],
      isDrawing: false,
    }
    console.log("LineDrawing constructor");
    console.log(this.state);
    this.canvasRef = React.createRef()
  }

  componentDidMount() {
    this.drawLines();
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.lines !== prevState.lines) {
      this.drawLines()
    }
  }

  handleMouseDown = (event) => {
    if (!this.getCurrentImage()) return
    const { offsetX, offsetY } = event.nativeEvent
    this.setState({
      isDrawing: true,
      lines: [
        ...this.state.lines,
        { start: { x: offsetX, y: offsetY }, end: null },
      ],
    })
  }

  handleMouseMove = (event) => {
    if (!this.state.isDrawing || !this.state.lines.length) return
    const { offsetX, offsetY } = event.nativeEvent
    this.setState((prevState) => ({
      lines: prevState.lines.map((line, index) =>
        index === prevState.lines.length - 1
          ? { ...line, end: { x: offsetX, y: offsetY } }
          : line
      ),
    }))
  }

  handleMouseUp = () => {
    this.setState({ isDrawing: false })
  }

  drawLines = () => {
    const canvas = this.canvasRef.current
    if (!canvas || !this.getCurrentImage()) return
    Streamlit.setComponentValue(this.state.lines)
    const ctx = canvas.getContext("2d")
    const currentImage = new Image()

    currentImage.onload = () => {
      canvas.width = currentImage.width
      canvas.height = currentImage.height
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      ctx.drawImage(currentImage, 0, 0)
      ctx.lineWidth = 2
      ctx.strokeStyle = "black"
      this.state.lines.forEach((line) => {
        if (line.end) {
          ctx.beginPath()
          ctx.moveTo(line.start.x, line.start.y)
          ctx.lineTo(line.end.x, line.end.y)
          ctx.stroke()
        }
      })
    }

    currentImage.src = `data:image/png;base64,${this.state.image}`
  }

  getCurrentImage() {
    return this.state.image
  }

  drawInitialImage = () => {
    const canvas = this.canvasRef.current

    const ctx = canvas.getContext("2d")
    const currentImage = new Image()

    currentImage.onload = () => {
      canvas.width = currentImage.width;
      canvas.height = currentImage.height;
      //ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(currentImage, 0, 0)
    }

    currentImage.onerror = (error) => {
      console.error("Error loading image:", error)
    }

    currentImage.src = `data:image/png;base64,${this.state.image}`
  }

  render() {
    return (
      <div id="draw_lines_container" style={{ textAlign: "left", width: this.state.width, height: this.state.height }}>
        {this.state.image && (
          <>
            <canvas
              ref={this.canvasRef}
              onMouseDown={this.handleMouseDown}
              onMouseMove={this.handleMouseMove}
              onMouseUp={this.handleMouseUp}
              style={{
                border: "3px solid black",
                cursor: "crosshair",
                height: this.state.image.height,
                width: this.state.image.width,
              }}
            />
            <button onClick={this.drawInitialImage}>Refresh</button>
          </>
        )}
      </div>
    )
  }
}

export default withStreamlitConnection(LineDrawing)
