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
      lines: [],
      isDrawing: false,
    }
    this.canvasRef = React.createRef()
  }

  componentDidUpdate(prevProps, prevState) {
    console.log("componentDidUpdate")

    if (prevState.currentImageIndex !== this.state.currentImageIndex) {
      this.drawLines()
    }
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
    console.log("drawLines func")
    const canvas = this.canvasRef.current
    if (!canvas || !this.getCurrentImage()) return
    const ctx = canvas.getContext("2d")
    const currentImage = new Image()

    currentImage.onload = () => {
      console.log("currentImage.onload");
      canvas.width = currentImage.width;
      canvas.height = currentImage.height;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(currentImage, 0, 0);
      ctx.lineWidth = 2;
      ctx.strokeStyle = "black";
      this.state.lines.forEach((line) => {
        console.log('line', line);
        if (line.end) {
          console.log('line.end', line.end);
          ctx.beginPath();
          ctx.moveTo(line.start.x, line.start.y)
          ctx.lineTo(line.end.x, line.end.y)
          ctx.stroke();
        }
      })
    }

    currentImage.src = `data:image/png;base64,${this.state.image}`
  }

  getCurrentImage() {
    return this.state.image
  }

  drawInitialImage = () => {
    console.log("drawInitialImage")
    const canvas = this.canvasRef.current

    const ctx = canvas.getContext("2d")
    const currentImage = new Image(400, 400)

    currentImage.onload = () => {
      canvas.width = currentImage.width
      canvas.height = currentImage.height
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
      <div style={{ textAlign: "center", height: "1000px" }}>
        {this.state.image && (
          <>
            {/* <img
              src={`data:image/png;base64,${this.state.image}`}
              alt="image"
            /> */}

            <canvas
              ref={this.canvasRef}
              backgroundColor="white"
              onMouseDown={this.handleMouseDown}
              onMouseMove={this.handleMouseMove}
              onMouseUp={this.handleMouseUp}
              style={{ border: "3px solid black", cursor: "crosshair" }}
            />
            <button onClick={this.drawInitialImage}>Refresh</button>

            {this.getCurrentImage() && (
              <div style={{ textAlign: "left", height: "1000px" }}>
                <h2>Line Segments:</h2>
                <ul>
                  {this.state.lines.map((line, index) => (
                    <li key={index}>
                      Start: ({line.start.x}, {line.start.y}) - End:{" "}
                      {line.end
                        ? `(${line.end.x}, {line.end.y})`
                        : "Not finished"}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </div>
    )
  }
}
Streamlit.setFrameHeight(1350)

export default withStreamlitConnection(LineDrawing)
